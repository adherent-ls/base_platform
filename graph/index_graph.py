from typing import List, Tuple, Optional, Union

from ..base_instance import ConvertInstance
from ..types.param_type import FilterType
from ..base_graph import BaseGraph
from ..instance.index_param_instance import input_types, output_types, filter_types


class IndexGraph(BaseGraph):
    def __init__(
            self,
            func: BaseGraph,
            ini: input_types,
            oui: output_types,
            fii: filter_types
    ):
        super().__init__()
        self.func = func
        self.ini = ini
        self.oui = oui
        self.fii = fii

    def forward(self, *data: List):
        input_data = ConvertInstance.list_extract(data, self.ini)
        func_data = self.func(*input_data)
        output_data = ConvertInstance.list_update(data, func_data, self.oui)
        filter_data = ConvertInstance.list_extract(output_data, self.fii)
        return filter_data


class SeriesWithIndexGraph(BaseGraph):
    def __init__(
            self,
            funcs: List[Union[
                Tuple[BaseGraph, input_types, output_types],
                Tuple[BaseGraph, input_types, output_types, filter_types],
            ]],
            ini: input_types,
            fii: filter_types = FilterType.All,
    ):
        super().__init__()
        self.ini = ini
        self.fii = fii
        for idx, item in enumerate(funcs):
            func, ini, oui = item[:3]
            if len(item) == 4:
                fii = item[3]
            else:
                fii = FilterType.All
            self.modules[str(idx)] = IndexGraph(func, ini, oui, fii)

    def forward(self, *data: List):
        data = ConvertInstance.list_extract(data, self.ini)
        for func in self.modules:
            data = func(*data)
        results = ConvertInstance.list_extract(data, self.fii)
        return results
