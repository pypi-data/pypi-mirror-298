from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentSpecificParametersEnum:
    SCIKIT = "scikit"
    STAN = "stan"
    CLAB_INPUT_FILE = "clab_input_file"
    DESCRIPTOR_TYPE = "descriptor_type"
    TRANSFORMATION = "transformation"

    # Chemaxon
    CHEMAXON_EXECUTOR_PATH = "chemaxon_executor_path"
    CHEMAXON_INPUT_MARKUSH_STRUCTURE_PATH = "chemaxon_input_markush_structure_path"
    CHEMAXON_TEMPORARY_FILES_PATH = "chemaxon_temporary_files_path"
    CHEMAXON_DEBUG = "chemaxon_debug"

    # structural components
    # ---------
    # AZDOCK
    AZDOCK_CONFPATH = "configuration_path"
    AZDOCK_DOCKERSCRIPTPATH = "docker_script_path"
    AZDOCK_ENVPATH = "environment_path"
    AZDOCK_DEBUG = "debug"

    # DockStream
    DOCKSTREAM_CONFPATH = "configuration_path"
    DOCKSTREAM_DOCKERSCRIPTPATH = "docker_script_path"
    DOCKSTREAM_ENVPATH = "environment_path"
    DOCKSTREAM_DEBUG = "debug"

    # ICOLOS
    ICOLOS_CONFPATH = "configuration_path"
    ICOLOS_EXECUTOR_PATH = "executor_path"
    ICOLOS_VALUES_KEY = "values_key"
    ICOLOS_DEBUG = "debug"
    #######################

    RAT_PK_PROPERTY = "rat_pk_property"
    CLAB_TOP_20_VALUE = "clab_top_20_value"
    ION_CLASS = "Ion class"
    CONTAINER_TYPE = "container_type"

    SMILES = "smiles"
    MODEL_PATH = "model_path"
    SIZE = "size"
    OUT_DIM = "out_dim"
    DROPOUT = "dropout"
    LAYERS = "layers"

    #######################
    PREDICTION_URL = "prediction_url"

    AIZYNTH_CONFIG_FILE_PATH = "aizynth_config_file_path"

    VALUE_MAPPING = "value_mapping"

    HITINVENT_REACTIONS_SET = "reactions_set"
    HITINVENT_BUILDING_BLOCKS_SET = "building_blocks_set"
    HITINVENT_NUMBER_OF_STEPS = "number_of_steps"
    HITINVENT_AIZYNTH_TIME_LIMIT_SECONDS = "time_limit_seconds"
    BACKEND = "backend"
