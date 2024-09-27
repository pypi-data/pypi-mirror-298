"""AiZynth REST API.

This module provides functions to call two AiZynth API:
- Batch tree API
- Batch expander API

AiZynth API documentation is at:
- https://confluence.astrazeneca.com/display/AIZ/AiZynthFinder+API (internal)

AiZynth API definitions could be found at:
- https://aizynth.dmta.astrazeneca.net/api/v1/schema/swagger-ui/ (internal)
- https://aizynth.dmta.astrazeneca.net/api/v2/schema/swagger-ui/ (internal)

AiZynth host for REST API is:
- https://aizynth.dmta.astrazeneca.net (internal)
"""

import os
from collections import defaultdict
from typing import List, Any, Dict

import requests
import tenacity as tenacity
from tenacity import retry_if_exception_type
from typing_extensions import TypedDict


# Environmental variables names.
AIZYNTH_TOKEN = "AIZYNTH_TOKEN"
AIZYNTH_BEARER_TOKEN = "AIZYNTH_BEARER_TOKEN"
AIZYNTH_HOST = "AIZYNTH_HOST"


# API endpoints.
EXPANDER_BATCH = "/api/v2/aizynthexpander/batch/"
CELERY_TASK = "/api/v2/celery/task/"
BUYABLES_LOOKUP = "/api/v2/buyables/lookup/"
AIZYNTH_TREE_BATCH = "/api/v1/aizynthfinder/trees/batch/"


# Type shortcuts.
SMILES = str
StockName = str
Stock = Dict[SMILES, List[StockName]]  # This is stock object we use for scoring.
RawStock = Dict[SMILES, List[Dict[str, Any]]]  # This is Json that API returns.


def aizynth_headers() -> Dict:
    """Returns request header for AiZynth.

    If permanent token available, returns dict for "Authorization: Token X".
    Otherwise, returns dict for "Authorization: Bearer X"
    with token from https://aizynth.dmta.astrazeneca.net .

    :return: header as a dict
    """

    if AIZYNTH_TOKEN in os.environ:
        auth = f"Token {os.environ[AIZYNTH_TOKEN]}"
    elif AIZYNTH_BEARER_TOKEN in os.environ:
        auth = f"Bearer {os.environ[AIZYNTH_BEARER_TOKEN]}"
    else:
        auth = ""

    headers = {
        "accept": "application/json",
        "Authorization": auth,
        "Content-Type": "application/json",
    }
    return headers


def aizynth_host() -> str:
    """Returns AiZynth host name

    :return: host
    """
    if AIZYNTH_HOST not in os.environ:
        raise ValueError(f"Environmental variable {AIZYNTH_HOST} is not set.")
    else:
        return os.environ[AIZYNTH_HOST]


class Reaction(TypedDict):
    """Reaction, as returned by AiZynth API"""

    rank: int
    smiles: str
    smiles_split: List[str]
    # ... and a bunch of other fields unused by Hitinvent.


ExpanderResponse = Dict[SMILES, List[Reaction]]


def expand(smiles: List[str]) -> ExpanderResponse:
    """Expands smiles into precursors by querying AiZynth.
    :param smiles: list of SMILES strings
    :return: JSON with AiZynth Expander response
    """

    task_id = submit_expander_request(smiles)
    data = get_expander_result(task_id)
    return data["output"]


def submit_expander_request(smiles: List[str]) -> str:
    """Submits request to AiZynth Batch Expander API and returns task id.
    :param smiles: list of SMILES strings
    :return: task id from the API
    """

    data = {
        "smiles": smiles,
        "first_n": 50,
    }
    response = requests.post(
        f"{aizynth_host()}{EXPANDER_BATCH}",
        headers=aizynth_headers(),
        json=data,
    )
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def submit_tree_request(smiles: List[str], depth: int) -> Dict[str, str]:
    """Submits request to AiZynth Batch Tree API and returns tree urls.
    :param smiles: list of SMILES strings
    :param depth: maximum depth of the synthesis tree
    :return: dict from SMILES string to tree URL
    """

    data = {
        "description": "Reinvent scoring",
        "settings": {
            "smiles": smiles,
            "max_transforms": depth,
            "return_first": False,
            "score_trees": False,
            "cluster_trees": False,
        },
    }
    response = requests.post(
        f"{aizynth_host()}{AIZYNTH_TREE_BATCH}",
        headers=aizynth_headers(),
        json=data,
    )
    response.raise_for_status()
    results = response.json()["results"]
    urls = {r["smiles"]: r["url"] for r in results}
    return urls


class ResultsStillPendingError(Exception):
    """Exception raised when results are still pending."""


@tenacity.retry(
    wait=tenacity.wait_fixed(5),
    retry=retry_if_exception_type(ResultsStillPendingError),
)
def get_tree(tree_url: str) -> Dict:
    """Returns synthesis tree(s) for one AiZynth url (one molecule).

    Retries if AiZynth status is "pending".

    :param tree_url: AiZynth URL for the tree
    :return: object representing JSON of AiZynth response
    """

    response = requests.get(
        tree_url,
        headers=aizynth_headers(),
    )
    response.raise_for_status()
    status = response.json()["state"]
    if status == "completed":
        return response.json()
    elif status == "pending":
        raise ResultsStillPendingError  # Retry with tenacity.
    else:
        raise ValueError(f"Unexpected AiZynth response status: {status}.")


@tenacity.retry(
    wait=tenacity.wait_fixed(5),
    retry=retry_if_exception_type(ResultsStillPendingError),
)
def get_expander_result(task_id: str) -> Dict:
    """Returns expander response.

    If expander results are not ready, resends the request.

    :param task_id: task id to build url (returned by expander batch API).
    :return: JSON from API response.
    """

    response = requests.get(
        f"{aizynth_host()}{CELERY_TASK}{task_id}",
        headers=aizynth_headers(),
    )
    response.raise_for_status()
    if not response.json()["complete"]:
        raise ResultsStillPendingError
    else:
        return response.json()


def fetch_stock(precursors: List[str]) -> Stock:
    """Returns stock from AiZynth API.

    :param precursors: list of SMILES strings
    :return: stock object
    """
    url = f"{aizynth_host()}{BUYABLES_LOOKUP}"
    data = {"smiles": precursors}
    print(f"Byables url: {url}, headers: {aizynth_headers()}, data: {data}")
    response = requests.post(
        url,
        headers=aizynth_headers(),
        json=data,
    )
    response.raise_for_status()
    res = response.json()["result"]
    # sources = {smi: [details["source"]] for smi, details in res.items()}
    # Do we need all/multiple sources per SMILES string?
    sources = defaultdict(list)  # Return empty list for missing compounds.
    for smi, details in res.items():
        sources[smi] = [avail["source"] for avail in details["available"]]

    return sources
