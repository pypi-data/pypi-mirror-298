import os
from abc import abstractmethod
from typing import List

import numpy as np
import requests

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.enums import EnvironmentalVariablesEnum
from reinvent_scoring.scoring.score_components.pip.base_rest_component import BaseRESTComponent


class PiPRequestError(Exception):
    pass


class BasePiPModelComponent(BaseRESTComponent):
    def __init__(self, parameters: ComponentParameters):
        self._environment_keys = EnvironmentalVariablesEnum()
        super().__init__(parameters)

    def _execute_request(self, request_url, data, header) -> dict:
        request = requests.post(request_url, json=data, headers=header)

        if request.status_code != 200:
            raise PiPRequestError(
                f"Component {self.parameters.component_type} failed.\n"
                f"Status Code: {request.status_code}\n"
                f"Reason: ({request.reason})\n"
                f"Response content: {request.content}\n"
                f"Response text: {request.text}"
            )

        return request.json()

    def _parse_response(self, response_json: dict, data_size: int) -> np.array:
        compounds = response_json['jsonData']['data']
        results_raw = np.empty(data_size, dtype=np.float32)
        results_raw[:] = np.nan

        try:
            for compound in compounds:
                try:
                    index = int(compound["id"])
                    results_raw[index] = self._parse_single_compound(compound)

                except (ValueError, TypeError, KeyError):
                    pass  # If parsing failed, keep value NaN for this compound and continue.
        finally:
            return results_raw

    @abstractmethod
    def _parse_single_compound(self, compound):
        raise NotImplementedError("_parse_compound method is not implemented")

    def _format_data(self, smiles: List[str]) -> dict:
        molecules = [{"molData": smi, "id": f"{i}"} for i, smi in enumerate(smiles)]
        data = {
            "jsonData": {
                "data": molecules,
                "metadata": {
                    "molFormat":
                        "smiles"
                },
                "parameters": {

                }
            }
        }
        return data

    def _create_url(self, async_path: str) -> str:
        pip_url = self._get_enviornment_variable(self._environment_keys.PIP_URL)
        request_url = pip_url.format(async_path)
        return request_url

    def _create_header(self) -> dict:
        pip_key = self._get_enviornment_variable(self._environment_keys.PIP_KEY)

        header = {
            'Content-Type': 'application/vnd.az.batch.v1+json', 'x-api-key': pip_key,
            'Accept': 'application/vnd.az.resultset.v1+json'
        }
        return header

    def _get_enviornment_variable(self, variable: str) -> str:
        try:
            return os.environ[variable]
        except KeyError:
            raise KeyError(f"Key {variable} not found in reinvent config")
