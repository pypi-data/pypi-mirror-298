from typing import List
from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components.pip.pip_prediction_component import PiPPredictionComponent


class QptunaPiPModelComponent(PiPPredictionComponent):

    def _create_url(self, async_path: str) -> str:
        return self.parameters.specific_parameters.get(
            self.component_specific_parameters.PREDICTION_URL)
