import numpy as np

import torch
from torch import nn

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem

from typing import List

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components import BaseScoreComponent
from reinvent_scoring.scoring.score_summary import ComponentSummary


class TorchQSARComponent(BaseScoreComponent):
    def __init__(self, parameters: ComponentParameters):
        super().__init__(parameters)
        self.activity_model = self._load_model()
        self._transformation_function = self._assign_transformation(parameters.specific_parameters)

    def calculate_score(self, molecules: List, step=-1) -> ComponentSummary:
        score = self._predict_and_transform(molecules)
        score_summary = ComponentSummary(
            total_score=score, parameters=self.parameters, raw_score=None
        )
        return score_summary

    def _predict_and_transform(self, molecules: List):

        fingerprints = [torch.FloatTensor(np.array(AllChem.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=2048))) for mol in molecules]
        print("\nFINGERPRINTS  COMPUTED")
        
        if "output_layer_1" in dict(self.activity_model.named_modules()):
            score = [torch.sigmoid(self.activity_model(mol, 1)).detach().cpu().numpy() for mol in fingerprints]
        else:
            score = [torch.sigmoid(self.activity_model(mol)).detach().cpu().numpy() for mol in fingerprints]
        print("\nSCORES  COMPUTED")
        return score

    def _load_model(self):
        model_path = self.parameters.specific_parameters.get(
            self.component_specific_parameters.MODEL_PATH, ""
        )
        #if "mf-DNN" in model_path:
        #    activity_model = MultiTask(input_size=2048, dropout=0.3).to("cpu")
        #else:
        #activity_model = SingleTask(input_size=2048, dropout=0.).to("cpu")
        activity_model = NonLinearNetDefer(input_dim=2048, out_dim=2, layers=[2, [1024, 512]], dropout=0.3).to("cpu")
        try:
            activity_model.load_state_dict(torch.load(model_path, map_location="cpu"))
            activity_model.eval()
        except:
            raise Exception(f"The loaded file `{model_path}` isn't a valid model")
        print("\nMODEL LOADED")
        return activity_model
    

class MultiTask(nn.Module):
    """
    Simple dense neural network for multitask classification.
    """

    def __init__(self, input_size:int, dropout:float=0.0):
        """
        Initialization.
        """
        super().__init__()
        self.input_layer = nn.Linear(input_size, 1024)
        self.hidden = nn.Sequential(
            nn.Linear(1024, 512),
            nn.SiLU(),
            nn.Dropout(dropout), # Add dropout to see effect on generalization.
            nn.Linear(512, 256),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.SiLU(),
        )

        self.output_layer_0 = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.output_layer_1 = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )


    def forward(self, x:torch.Tensor, task_id:int):
        """
        Forward pass.
        """
        x = self.input_layer(x)
        x = self.hidden(x)
        if task_id == 0:
            logits = self.output_layer_0(x)
        elif task_id == 1:
            logits = self.output_layer_1(x)
        
        return logits


class SingleTask(nn.Module):
    """
    Simple dense neural network for single task classification.
    """

    def __init__(self, input_size:int, dropout:float=0.0):
        """
        Initialization.
        """
        super().__init__()
        self.input_layer = nn.Linear(input_size, 512)
        self.hidden = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(dropout), # Add dropout to see effect on generalization.
            nn.Linear(256, 64),
            nn.ELU()
        )

        self.output_layer = nn.Linear(64, 1)

    def forward(self, x:torch.Tensor):
        """
        Forward pass.
        """
        x = self.input_layer(x)
        x = self.hidden(x)
        logits = self.output_layer(x)
        
        return logits
