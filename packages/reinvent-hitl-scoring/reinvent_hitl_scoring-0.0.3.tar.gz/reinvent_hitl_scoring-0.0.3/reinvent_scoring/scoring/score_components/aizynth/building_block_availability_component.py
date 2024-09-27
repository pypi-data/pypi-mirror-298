"""Scoring component that uses AiZynth for retro synthesis planning.

The following backends implemented:
- AiZynth Batch tree REST API
- AiZynth Batch expander REST API
- AiZynthFinder CLI API on SCP with AiZynthFinder's built-in parallelization
- AiZynthFinder CLI API on SCP with SLURM parallelization
"""

import logging
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import List, Iterable, Set

import numpy as np
from pkg_resources import resource_string

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components.aizynth.aizynth_cli_api import (
    run_aizynthfinder_array,
    run_aizynthfinder_preallocated,
)
from reinvent_scoring.scoring.score_components.aizynth.aizynth_rest_api import (
    expand,
    fetch_stock,
    Reaction,
    Stock,
    submit_tree_request,
    get_tree,
)
from reinvent_scoring.scoring.score_components.aizynth.util import (
    extract_startmat,
    extract_reaction_metadata,
    extract_reacticlass,
    flatten_stock,
    flatten_precursors,
    code_from_classification,
)
from reinvent_scoring.scoring.score_components.base_score_component import (
    BaseScoreComponent,
)
from reinvent_scoring.scoring.score_summary import ComponentSummary

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def ilab_compatible_reaction_classes() -> Set[str]:
    """Returns ILAB compatible reaction classes from accompanying data file

    Data file lists reaction classes, one per line.
    Each line starts with a code, and can have a description, separated by space.
    Example file:
        1.1.1
        1.2.1

    :return: a Set of reaction classes as strings
    """
    lines = (
        resource_string(
            "reinvent_scoring.scoring.score_components.aizynth",
            "ilab_compatible_reactions.txt",
        )
        .decode("utf-8")
        .splitlines()
    )
    codes = {code_from_classification(c) for c in lines}
    return codes


@dataclass
class BblockScore:
    """Building block scoring profile."""

    ISAC: float  # Best for iLAB.
    ERM: float  # "Easy" to use if the site is the same as the user.
    ACD: float  # Externally buy-able.
    missing: float  # Missing from any stock (also unrecognized stock).

    def getmax(self, sources: Iterable[str]) -> float:
        sscores = {
            "ISAC": self.ISAC,
            "ERM": self.ERM,
            "ACD": self.ACD,
        }
        scores = [sscores.get(s, self.missing) for s in sources]
        return max(scores, default=self.missing)


internal_az_only = BblockScore(ISAC=1.0, ERM=0.99, ACD=0.3, missing=0.1)
external_buyable = BblockScore(ISAC=1.0, ERM=0.99, ACD=0.8, missing=0.1)


class BuildingBlockSets(str, Enum):
    INTERNAL_AZ_ONLY = "internal_az_only"
    EXTERNAL_BUYABLE = "external_buyable"


class ReactionSets(str, Enum):
    ILAB_COMPATIBLE = "ilab_compatible"
    ANY = "any"


class AiZynthBackend(str, Enum):
    AIZYNTH_REST_BATCH_TREE = "aizynth_rest_batch_tree"
    AIZYNTH_REST_BATCH_EXPANDER = "aizynth_rest_batch_expander"
    AIZYNTHFINDER_CLI_SCP_PREALLOCATED = (
        "aizynthfinder_cli_on_scp_use_parent_allocation"
    )
    AIZYNTHFINDER_CLI_SCP_ALLOCATE = (
        "aizynthfinder_cli_on_scp_reallocate_for_every_batch"
    )


class BuildingBlockAvailabilityComponent(BaseScoreComponent):
    """AiZynth one-step synthesis building block availability.

    Score is the ratio between
    the number of reactants in stock
    and the number of all reactants.

    If a molecule can be synthesized using different reactions,
    with different sets of reactants,
    the maximum ratio is used.

    This scoring component uses AiZynthFinder Expansion interface:
    https://molecularai.github.io/aizynthfinder/python_interface.html#expansion-interface
    """

    def __init__(self, parameters: ComponentParameters):
        super().__init__(parameters)
        self._reactions_set = self.parameters.specific_parameters.get(
            self.component_specific_parameters.HITINVENT_REACTIONS_SET,
            ReactionSets.ILAB_COMPATIBLE,
        )
        self._building_blocks_set = self.parameters.specific_parameters.get(
            self.component_specific_parameters.HITINVENT_BUILDING_BLOCKS_SET,
            BuildingBlockSets.INTERNAL_AZ_ONLY,
        )
        self._number_of_steps = self.parameters.specific_parameters.get(
            self.component_specific_parameters.HITINVENT_NUMBER_OF_STEPS, 3
        )
        self._backend = self.parameters.specific_parameters.get(
            self.component_specific_parameters.BACKEND,
            AiZynthBackend.AIZYNTHFINDER_CLI_SCP_ALLOCATE,
        )
        self._time_limit_seconds = self.parameters.specific_parameters.get(
            self.component_specific_parameters.HITINVENT_AIZYNTH_TIME_LIMIT_SECONDS, 60
        )

    def calculate_score(self, molecules: List, step=-1) -> ComponentSummary:
        valid_smiles = self._chemistry.mols_to_smiles(molecules)

        if self._backend in {
            AiZynthBackend.AIZYNTHFINDER_CLI_SCP_ALLOCATE,
            AiZynthBackend.AIZYNTHFINDER_CLI_SCP_PREALLOCATED,
        }:
            score = self._score_smiles_aizynthfinder(valid_smiles)
        elif self._backend == AiZynthBackend.AIZYNTH_REST_BATCH_TREE:
            score = self._score_smiles_batchtree(valid_smiles)
        elif self._backend == AiZynthBackend.AIZYNTH_REST_BATCH_EXPANDER:
            if self._number_of_steps == 1:
                score = self._score_smiles_expander(valid_smiles)
            else:
                raise ValueError(
                    f"Selected AiZynth Expander backend,"
                    f" but number of steps {self._number_of_steps} != 1."
                )
        else:
            raise ValueError(f"Unrecognized AiZynth backend: {self._backend}.")

        score_summary = ComponentSummary(
            total_score=score, parameters=self.parameters, raw_score=score
        )

        return score_summary

    def _score_smiles_batchtree(self, smiles: List[str]) -> np.ndarray:
        urls = submit_tree_request(smiles, depth=self._number_of_steps)
        scores = []
        for smi in smiles:
            try:
                score = self._score_one_smi(get_tree(urls[smi]))  # Could be async.
            except Exception as e:
                logger.warning(
                    "AiZynth scoring component could not compute score for %s.",
                    smi,
                    exc_info=e,
                )
                score = 0
            scores.append(score)

        return np.array(scores)

    def _score_smiles_expander(self, smiles: List[str]) -> np.ndarray:
        output = expand(smiles)
        stock = fetch_stock(flatten_precursors(output))
        scores = [self._score_one_smi_expander(output[smi], stock) for smi in smiles]
        return np.array(scores)

    def _score_one_smi(self, tree_response) -> float:
        """Score one compound.

        One compound can have multiple synthesis trees,
        we return score of the best tree.
        """

        rawstock = tree_response["result"]["stock"]["smiles"]
        stock = flatten_stock(rawstock)
        trees = tree_response["result"]["trees"]
        scores = []
        for t in trees:
            bblocks = extract_startmat(t)
            bblock_sources = [stock.get(b, []) for b in bblocks]
            rmetadata = extract_reaction_metadata(t)
            rclasses = extract_reacticlass(rmetadata)
            num_steps = len(rmetadata)
            score = self._score_one_tree(bblock_sources, rclasses, num_steps)
            scores.append(score)

        return max(scores, default=0)

    def _score_smiles_aizynthfinder(self, smiles: List[str]) -> np.ndarray:

        if self._backend == AiZynthBackend.AIZYNTHFINDER_CLI_SCP_ALLOCATE:
            out = run_aizynthfinder_array(smiles, self._time_limit_seconds)
        elif self._backend == AiZynthBackend.AIZYNTHFINDER_CLI_SCP_PREALLOCATED:
            out = run_aizynthfinder_preallocated(smiles, self._time_limit_seconds)
        else:
            raise ValueError(f"Unrecognized backend: {self._backend}")

        all_scores = {}
        for mol in out["data"]:
            smi = mol["target"]
            trees = mol["trees"]
            stock = mol["stock_info"]
            scores = []
            for t in trees:
                bblocks = extract_startmat(t)
                bblock_sources = [stock.get(smi, []) for smi in bblocks]
                rmetadata = extract_reaction_metadata(t)
                rclasses = extract_reacticlass(rmetadata)
                num_steps = len(rmetadata)
                score = self._score_one_tree(bblock_sources, rclasses, num_steps)
                scores.append(score)

            all_scores[smi] = max(scores, default=0)

        ordered_scores = []
        for smi in smiles:
            s = all_scores.get(smi, None)
            if s is None:
                logger.warning(f"Missing score for {smi}")
                ordered_scores.append(0)
            else:
                ordered_scores.append(s)
        return np.array(ordered_scores)

    def _score_one_smi_expander(self, data: List[Reaction], stock: Stock) -> float:
        scores = []  # List of scores, one score for one reaction.
        for r in data:
            bblocks = r["smiles_split"]
            bblock_sources = [stock[smi] for smi in bblocks]
            rclasses = (
                []
            )  # Expander do not return classes, let's consider all compatible.
            num_steps = 1  # Expander returns 1-step routes only.
            score = self._score_one_tree(bblock_sources, rclasses, num_steps)
            scores.append(score)

        return max(scores, default=0)

    def _score_one_tree(
        self,
        bblock_sources: Iterable[Iterable[str]],
        rclasses: Iterable[str],
        num_steps: int,
    ) -> float:
        """Scores one tree.

        :param bblock_sources: list of sources for each building block (BB)
        :param rclasses: reaction classes as list of numeric NextMove codes
        :param num_steps: number of synthesis steps (depth of synthesis tree)
        :return: score
        """

        score = 1.0

        # Score by building blocks
        if self._building_blocks_set == BuildingBlockSets.INTERNAL_AZ_ONLY:
            bblock_score = internal_az_only
        elif self._building_blocks_set == BuildingBlockSets.EXTERNAL_BUYABLE:
            bblock_score = external_buyable
        else:
            raise ValueError(
                f"Unrecognized building blocks set: {self._building_blocks_set}"
            )
        for sources in bblock_sources:
            s = bblock_score.getmax(sources)
            score *= s

        # Score by reaction classes.
        for c in rclasses:
            if self._reactions_set == ReactionSets.ILAB_COMPATIBLE:
                s = 1 if c in ilab_compatible_reaction_classes() else 0.1
                score *= s

        # Score by number of steps.
        # Hard cut-off on aizynth size.
        # We can add "soft" signal to reward fewer steps.
        score *= 0.98**num_steps

        return score
