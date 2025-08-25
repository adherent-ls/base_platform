from typing import List, Tuple, Optional

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
            ini: InputInstance,
            funcs: List[Tuple[
                BaseGraph,
                Optional[InputInstance],
                Optional[OutputInstance],
                Optional[FilterInstance]
            ]]
    ):
        super().__init__()
        self.ini = ini
        for idx, item in enumerate(funcs):
            self.modules[str(idx)] = IndexGraph(*item)

    def forward(self, *data: List):
        data = self.ini.data_format(data)
        for func in self.modules:
            data = func(*data)
        return data
