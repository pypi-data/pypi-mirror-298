import csv
import os
import shutil
import subprocess

import numpy as np
from typing import List, Tuple
import re
import pandas as pd

from reinvent_scoring.scoring.enums import EnvironmentalVariablesEnum
from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components.console_invoked.base_console_invoked_component import BaseConsoleInvokedComponent
from reinvent_chemistry.conversions import Conversions


class Chemaxon(BaseConsoleInvokedComponent):
    def __init__(self, parameters: ComponentParameters):
        super().__init__(parameters)
        self._executor_path = self.parameters.specific_parameters[self.component_specific_parameters.CHEMAXON_EXECUTOR_PATH]
        self._markush_structure_path = self.parameters.specific_parameters[self.component_specific_parameters.CHEMAXON_INPUT_MARKUSH_STRUCTURE_PATH]
        self._mapping = self.parameters.specific_parameters.get(self.component_specific_parameters.VALUE_MAPPING, {'Match': 1.0, 'Not Match': 0.5})
        self._chemaxon_debug = self.parameters.specific_parameters.get(self.component_specific_parameters.CHEMAXON_DEBUG, False)
        self._temporary_files_path = self.parameters.specific_parameters[self.component_specific_parameters.CHEMAXON_TEMPORARY_FILES_PATH]
        self._environment_keys = EnvironmentalVariablesEnum()
        self._chemistry = Conversions()

    def _create_command(self, input_sdf_path: str, input_markush_structure_path: str, output_path: str):
        command = f'java -jar {self._executor_path} search {input_sdf_path} {input_markush_structure_path} > {output_path}'
        return command

    def _calculate_score(self, molecules: List, step: int) -> Tuple[np.ndarray, np.ndarray]:
        if not os.path.exists(self._temporary_files_path):
            os.makedirs(self._temporary_files_path)
        input_sdf_path = os.path.join(self._temporary_files_path, "chemaxon_input.sdf")
        output_txt_path = os.path.join(self._temporary_files_path, "chemaxon_output.txt")

        # write molecules to sdf format file input_sdf_path
        self._chemistry.mol_to_sdf(molecules, input_sdf_path)

        # create the external command
        command = self._create_command(input_sdf_path, self._markush_structure_path, output_txt_path)

        # execute Chemaxon markush structure searching
        self._execute_command(command=command)

        # parse the output txt to csv
        csv_result_path = os.path.join(self._temporary_files_path, 'chemaxon_output.csv')
        self._parse_output_txt_to_csv(output_txt_path, csv_result_path)

        # get match score (0.5 for not matching or 1 for matching default) from csv file
        score = self._get_match_result_from_csv(csv_result_path)

        # clean up
        if not self._chemaxon_debug:
            self._clean_up_temporary_folder(self._temporary_files_path)

        return score, None

    def _get_match_result_from_csv(self, converted_result_csv_file):
        result_df = pd.read_csv(converted_result_csv_file)

        matches = []
        for element in result_df['Matching'].tolist():
            if element == 'YES':
                matches.append(self._mapping['Match'])
            elif element == 'NO':
                matches.append(self._mapping['Not Match'])
        return np.array(matches)

    def _parse_output_txt_to_csv(self, txt_path: str, csv_path: str):
        """
        txt to be parsed looks like:
        Searching Markush structures...
        Input file:            x.sdf
        Markush directory:     y

        Input molecule count:  30
        Markush count:         1

        Molecule    Time            Matching    Markush structure(s)
               1    00:00:00.872    YES         WO2017153527
               2    00:00:00.599    YES         WO2017153527
        """
        with open(txt_path) as f:
            lines = f.readlines()

        start_row = 'Molecule Time Matching Markush structure(s)'
        start_row_index = 0
        for i, line in enumerate(lines):
            line = re.sub(' +', ' ', line).strip()
            if line == start_row:
                start_row_index = i
                break
        if i == len(lines)-1:
            raise IOError(f"{txt_path} must contain '{start_row}'")

        processed_lines = ['Molecule Time Matching Markush_structure(s)']
        for j in range(start_row_index+1, len(lines)):
            if lines[j] != '\n':
                temp = re.sub(' +', ' ', lines[j]).strip()
                processed_lines.append(temp)
            else:
                break

        converted_result = (line.split(" ") for line in processed_lines)
        with open(csv_path, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(converted_result)

    def _execute_command(self, command: str):
        JAVA_HOME = self._get_enviornment_variable('JAVA_HOME')
        my_env = os.environ.copy()
        my_env["PATH"] = f"{JAVA_HOME}/bin:" + my_env["PATH"]
        subprocess.run(command, shell=True, env=my_env)

    def _get_enviornment_variable(self, variable: str) -> str:
        try:
            return os.environ[variable]
        except KeyError:
            raise KeyError(f"Key {variable} not found in reinvent config")

    def _clean_up_temporary_folder(self, temporary_folder):
        if os.path.isdir(temporary_folder):
            shutil.rmtree(temporary_folder)
