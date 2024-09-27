from typing import Dict, Any

from reinvent_scoring.scoring.enums.container_type_enum import ContainerType
from reinvent_scoring.scoring.enums.component_specific_parameters_enum import ComponentSpecificParametersEnum

from reinvent_scoring.scoring.predictive_model.base_model_container import BaseModelContainer
from reinvent_scoring.scoring.predictive_model.optuna_container import OptunaModelContainer
from reinvent_scoring.scoring.predictive_model.scikit_model_container import ScikitModelContainer
from reinvent_scoring.scoring.predictive_model.stan_model_container import StanModelContainer
from reinvent_scoring.scoring.predictive_model.torch_model_container import TorchModelContainer
from reinvent_scoring.scoring.predictive_model.ensemble_model_container import EnsembleModelContainer
from reinvent_scoring.scoring.predictive_model.imbalanced_model_container import ImbalancedModelContainer


class ModelContainer:

    def __new__(cls, activity_model: Any, specific_parameters: Dict) -> BaseModelContainer:
        _component_specific_parameters = ComponentSpecificParametersEnum()
        _container_type = ContainerType()
        container_type = specific_parameters.get(_component_specific_parameters.CONTAINER_TYPE,
                                                 _container_type.STAN_CONTAINER)
        if container_type == _container_type.SCIKIT_CONTAINER:
            container_instance = ScikitModelContainer(activity_model,
                                                      specific_parameters[_component_specific_parameters.SCIKIT],
                                                      specific_parameters)
        if container_type == _container_type.OPTUNA_CONTAINER:
            # TODO: possibly a good spot for error try/catching
            container_instance = OptunaModelContainer(activity_model)
        if container_type == _container_type.STAN_CONTAINER:
            container_instance = StanModelContainer(activity_model,
                                                    specific_parameters)
        if container_type == _container_type.TORCH_CONTAINER:
            container_instance = TorchModelContainer(activity_model, specific_parameters)
        if container_type == _container_type.ENSEMBLE_CONTAINER:
            container_instance = EnsembleModelContainer(activity_model, specific_parameters[_component_specific_parameters.SCIKIT], specific_parameters)
        if container_type == _container_type.IMBALANCED_CONTAINER:
            container_instance = ImbalancedModelContainer(activity_model, specific_parameters[_component_specific_parameters.SCIKIT], specific_parameters)


        return container_instance
