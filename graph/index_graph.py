from typing import List, Tuple, Optional, Union

from ..base_graph import BaseGraph
from ..instance.index_param_instance import InputInstance, OutputInstance, FilterInstance


class IndexGraph(BaseGraph):
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

    def forward(self, *data: List):
        input_data = self.ini.extract_data(data)
        func_data = self.func(*input_data)
        output_data = self.oui.update_data(data, func_data)
        filter_data = self.fii.filter_data(output_data)
        return filter_data


class SeriesWithIndexGraph(BaseGraph):
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
            func, ini, oui = item[:3]
            ini = InputInstance(ini)
            oui = OutputInstance(oui)
            if len(item) == 4:
                fii = FilterInstance(item[3])
            else:
                fii = FilterInstance()
            self.modules[str(idx)] = IndexGraph(func, ini, oui, fii)

    def forward(self, *data: List):
        data = InputInstance.data_format(data, self.ini)
        for func in self.modules:
            data = func(*data)
        results = OutputInstance.extract_data(data, self.oui)
        return results
