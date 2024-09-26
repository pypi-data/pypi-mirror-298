from dataclasses import dataclass

from lisa.globalfit.framework.msg.data import ModuleState


@dataclass
class ModuleConfiguration:
    group_label: str
    module_label: str
    initial_state: ModuleState
    static_configuration_reference: str


@dataclass
class PreprocessorOutput:
    modules: list[ModuleConfiguration]
