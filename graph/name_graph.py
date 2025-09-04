from typing import List, Dict, Tuple, Union

from ..types.base_param_type import FilterType
from ..base_instance import ConvertInstance
from ..base_graph import BaseGraph
from types.name_param_instance import input_types, output_types, filter_types


class NameGraph(BaseGraph):
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

    def forward(self, **data: Dict):
        input_data = ConvertInstance.dict_to_list(data, self.ini)
        func_data = self.func(*input_data)
        output_data = ConvertInstance.dict_update(data, func_data, self.oui)
        filter_data = ConvertInstance.dict_extract(output_data, self.fii)
        return filter_data


class SeriesWithNameGraph(BaseGraph):
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
            self.modules[str(idx)] = NameGraph(func, ini, oui, fii)

    def forward(self, *data: List):
        data_dict = ConvertInstance.list_to_dict(data, self.ini)
        for name, func_item in self.modules.items():
            data_dict = func_item(**data_dict)
        result = ConvertInstance.dict_to_list(data_dict, self.fii)
        return result
