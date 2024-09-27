from typing import Dict, Set, List

from typing_extensions import TypedDict

from reinvent_scoring.scoring.score_components.aizynth.aizynth_rest_api import (
    RawStock,
    Stock,
    ExpanderResponse,
)


class ReactionMetadata(TypedDict):
    classification: str
    # ... more elements, unused here.


def extract_startmat(tree: Dict) -> Set[str]:
    """Returns all starting materials for a synthesis tree.

    Starting material is returned as a set of SMILES string of all leaf nodes.
    :param tree: synthhesis tree
    :return: set of SMILES strings of starting materials
    """

    def traverse(tree: Dict, leaves: Set) -> None:
        children = tree.get("children", [])
        if children:
            for child in children:
                traverse(child, leaves)
        else:
            leaves.add(tree["smiles"])

    startmat = set()
    traverse(tree, startmat)
    return startmat


def extract_reaction_metadata(tree: Dict) -> List[ReactionMetadata]:
    """Extract a list of metadata for all reactions in a synthesis tree.

    Metadata is returned as a list of metadata dictionaries
    from reactions in the tree.

    :param tree: synthesis tree
    :return: list of metadata dictionaries
    """

    def traverse(tree: Dict, metadata: List) -> None:
        # 'metadata' is a mutable list to collect output.
        if tree["type"] == "reaction":
            metadata.append(tree["metadata"])

        for child in tree.get("children", []):
            traverse(child, metadata)

    metadata = []
    traverse(tree, metadata)
    return metadata


def code_from_classification(classification: str) -> str:
    """Returns reaction code from reaction classification string.

    Example of classification string:
        1.6.2 Bromo N-alkylation

    :param classification: classification string
    ":return: reaction code
    """
    return classification.split(" ")[0]


def code_from_metadata(metadata: ReactionMetadata) -> str:
    """Returns numeric code from NextMove classification.

    :param metadata: reaction metadata dict
    :return: reaction classification code
    """

    classification = metadata.get("classification", None)
    if classification is None:
        return "Unclassified"
    else:
        return code_from_classification(classification)


def extract_reacticlass(metadata: List[ReactionMetadata]) -> List[str]:
    """Returns a list of reaction classes for metadata dictionaries.
    :param metadata: list of metadata dicts
    :return: list of reaction classification codes
    """

    classes = [code_from_metadata(m) for m in metadata]
    return classes


def flatten_stock(rawstock: RawStock) -> Stock:
    """Returns Stock object from "raw" stock.
    :param rawstock: "raw" stock as returned by AiZynth
    :return: stock object with only sources
    """

    stock = {m: [s["source"] for s in rawstock[m]] for m in rawstock.keys()}
    return stock


def flatten_precursors(data: ExpanderResponse) -> List[str]:
    """Returns all molecules seen in expander response.

    This flat list of precursors is used to fetch stock availability.
    :param data: expander response
    :return: list of SMILES strings
    """
    precursors = []
    for smi, reactions in data.items():
        precursors.append(smi)
        for p in reactions:
            precursors.extend(p["smiles_split"])
    return list(set(precursors))
