from enum import Enum
from typing import Union, List, Dict, Tuple

from base.base_graph import BaseGraph


class UseField(object):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg


class FilterType(Enum):
    All: str = 'All'
    No: str = 'No'


class KeepType(Enum):
    All: str = 'All'
    Instance: str = 'Instance'


class IndexGraph(BaseGraph):
    def __init__(
            self,
            func,
            in_indices: List[Union[int, UseField]],
            out_indices: Union[int, List[Union[int, UseField]]],
            filter: Union[str, List[int]] = FilterType.All
    ):
        super().__init__()
        self.in_indices = in_indices
        self.out_indices = out_indices
        self.filter = filter
        self.func = func

    def input_data(self, data: Union[Tuple, List]):
        if isinstance(self.in_indices, List):
            data_item = []
            for index in self.in_indices:
                if isinstance(index, int):
                    data_item.append(data[index])
                elif isinstance(index, UseField):
                    data_item.append(index.arg)
                else:
                    raise NotImplemented
        else:
            raise NotImplemented
        return data_item

    def output_data(self, data: Union[Tuple, List], func_output: List):
        if self.filter == FilterType.All:
            result = list(data)
        elif self.filter == FilterType.No:
            result = []
        elif isinstance(self.filter, List):
            result = []
            for item in self.filter:
                result.append(data[item])
        else:
            raise NotImplemented

        if isinstance(self.out_indices, int):
            result[self.out_indices] = func_output
        elif isinstance(self.out_indices, List):
            for i, name in enumerate(self.out_indices):
                result[name] = func_output[i]
        else:
            raise NotImplemented
        return result

    def forward(self, *data: List):
        data_item = self.input_data(data)
        data_item = self.func(*data_item)
        result = self.output_data(data, data_item)
        return result


class SeriesWithIndexGraph(BaseGraph):
    def __init__(self,
                 funcs: List,
                 input_indices: List[int],
                 keep: Union[KeepType, int, List[int]] = KeepType.All
                 ):
        super().__init__()
        self.input_indices = input_indices
        self.keep = keep
        self.funcs = [IndexGraph(*item) for item in funcs]

    def input_data(self, data: Union[Tuple, List]):
        return [data[index] for index in self.input_indices]

    def output_data(self, func_output: List):
        if self.keep == KeepType.All:
            result = func_output
        elif isinstance(self.keep, int):
            result = func_output[self.keep]
        elif isinstance(self.keep, List):
            result = []
            for i, index in enumerate(self.keep):
                result.append(func_output[index])
        else:
            raise NotImplemented
        return result

    def forward(self, *data: List):
        data = self.input_data(data)
        for func in self.funcs:
            data = func(*data)
        result = self.output_data(data)
        return result


class NameGraph(BaseGraph):
    def __init__(
            self,
            func,
            in_names: List[Union[str, UseField]],
            out_names: Union[str, List[str]],
            filter: Union[FilterType, List[str]] = FilterType.All
    ):
        super().__init__()
        self.in_names = in_names
        self.out_names = out_names
        self.filter = filter
        self.func = func

    def input_data(self, data: Dict):
        if isinstance(self.in_names, List):
            data_item = []
            for name in self.in_names:
                if isinstance(name, str):
                    data_item.append(data[name])
                elif isinstance(name, UseField):
                    data_item.append(name.arg)
                else:
                    raise NotImplemented
        else:
            raise NotImplemented
        return data_item

    def output_data(self, data: Dict, func_output: Union[object, List]):
        if self.filter == FilterType.All:
            result = data
        elif self.filter == FilterType.No:
            result = {}
        elif isinstance(self.filter, List):
            result = {}
            for item in self.filter:
                result[item] = data[item]
        else:
            raise NotImplemented

        if isinstance(self.out_names, str):
            result[self.out_names] = func_output
        elif isinstance(self.out_names, List):
            for i, name in enumerate(self.out_names):
                result[name] = func_output[i]
        else:
            raise NotImplemented
        return result

    def forward(self, **data: Dict):
        input_data = self.input_data(data)
        func_data = self.func(*input_data)
        output_data = self.output_data(data, func_data)
        return output_data

    def extra_repr(self) -> str:
        # 这里放一些你希望展示的属性
        name = self.func.__name__ if hasattr(self.func, '__name__') else self.func.__class__.__name__
        in_names = []
        for item in self.in_names:
            if isinstance(item, UseField):
                in_names.append(item.arg)
            else:
                in_names.append(item)
        return (f"{name}{*in_names,} -> {self.out_names}")


class SeriesWithNameGraph(BaseGraph):
    def __init__(
            self,
            funcs,
            input_names: List[str],
            keep: Union[KeepType, str, List[str]] = KeepType.All
    ):
        super().__init__()
        self.input_names = input_names
        self.keep = keep
        for idx, item in enumerate(funcs):
            self.modules[str(idx)] = NameGraph(*item)

    def input_data(self, data: Union[Tuple, List]):
        return {name: item for name, item in zip(self.input_names, data)}

    def output_data(self, func_output: Dict):
        if self.keep == KeepType.All:
            result = list(func_output.values())
        elif isinstance(self.keep, str):
            result = func_output[self.keep]
        elif isinstance(self.keep, List):
            result = []
            for i, name in enumerate(self.keep):
                result.append(func_output[name])
        else:
            raise NotImplemented
        return result

    def forward(self, *data: List):
        data_dict = self.input_data(data)
        for name, func_item in self.modules.items():
            data_dict = func_item(**data_dict)
        result = self.output_data(data_dict)
        return result


class SeriesListGraph(BaseGraph):
    def __init__(self, funcs: List):
        super().__init__()
        self.funcs = funcs

    def forward(self, *data: any):
        for func in self.funcs:
            data = func(*data)
        return data


class IterationGraph(BaseGraph):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def forward(self, *data):
        new_data = []
        for item in zip(*data):
            new_data.append(self.func(*item))
        return new_data


class ParallelGraph(BaseGraph):
    def __init__(self, funcs):
        super().__init__()
        self.funcs = funcs

    def forward(self, data):
        items = []
        for func in self.funcs:
            item = func(data)
            items.append(item)
        return items


class MergeGraph(BaseGraph):
    def __init__(self, funcs, in_indices):
        super().__init__()
        self.funcs = funcs
        self.in_indices = in_indices

    def forward(self, data):
        data_item = []
        if isinstance(self.in_indices, int):
            data_item.append(data)
        else:
            for index in self.in_indices:
                data_item.append(data[index])

        result = 0
        for item in self.funcs:
            func, weight = item
            result += func(*data_item) * weight
        return result
