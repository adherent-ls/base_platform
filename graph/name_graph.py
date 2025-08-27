from typing import List, Dict, Tuple, Union

from ..base_graph import BaseGraph
from ..instance.name_param_instance import InputInstance, OutputInstance, FilterInstance


class NameGraph(BaseGraph):
    def __init__(
            self,
            func: BaseGraph,
            ini: InputInstance = InputInstance(),
            oui: OutputInstance = OutputInstance(),
            fii: FilterInstance = FilterInstance()
    ):
        super().__init__()
        self.func = func
        self.ini = ini
        self.oui = oui
        self.fii = fii

    def forward(self, **data: Dict):
        input_data = self.ini.extract_data(data)
        func_data = self.func(*input_data)
        output_data = self.oui.update_data(data, func_data)
        filter_data = self.fii.filter_data(output_data)
        return filter_data


class SeriesWithNameGraph(BaseGraph):
    def __init__(
            self,
            funcs: List[Union[
                Tuple[BaseGraph, InputInstance.types, OutputInstance.types],
                Tuple[BaseGraph, InputInstance.types, OutputInstance.types, FilterInstance.types],
            ]],
            ini: InputInstance.types,
            oui: OutputInstance.types = None,
    ):
        super().__init__()
        self.ini = ini
        self.oui = oui
        for idx, item in enumerate(funcs):
            func, ini, oui, fii = item
            ini = InputInstance(ini)
            oui = OutputInstance(oui)
            fii = FilterInstance(fii)
            self.modules[str(idx)] = NameGraph(func, ini, oui, fii)

    def forward(self, *data: List):
        data_dict = self.ini.data_format(data)
        for name, func_item in self.modules.items():
            data_dict = func_item(**data_dict)
        result = OutputInstance.extract_data(data_dict, self.oui)
        return result
