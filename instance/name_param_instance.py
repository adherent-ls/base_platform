from typing import List, Union, Dict

from ..base_instance import BaseInstance
from ..types.param_type import FilterType, UseField


class InputInstance(BaseInstance):
    types = List[Union[str, UseField]]

    def __init__(self, names: types = ()):
        super().__init__()
        self.names = names

    def extract_data(self, data):
        if isinstance(self.names, List):
            data_item = []
            for name in self.names:
                if isinstance(name, str):
                    data_item.append(data[name])
                elif isinstance(name, UseField):
                    data_item.append(name.arg)
                else:
                    raise NotImplemented
        else:
            raise NotImplemented
        return data_item

    @staticmethod
    def data_format(data, names):
        return {name: item for name, item in zip(names, data)}


class OutputInstance(BaseInstance):
    types = Union[str, List[str]]

    def __init__(self, names: types = ()):
        super().__init__()
        self.names = names

    def update_data(self, result, func_output):
        if isinstance(self.names, str):
            result[self.names] = func_output
        elif isinstance(self.names, List):
            for i, name in enumerate(self.names):
                result[name] = func_output[i]
        else:
            raise NotImplemented
        return result

    @staticmethod
    def extract_data(data: Dict, names: types):
        if names is None:
            results = data.values()
        elif isinstance(names, str):
            results = data[names]
        elif isinstance(names, List):
            results = []
            for i, name in enumerate(names):
                results.append(data[name])
        else:
            raise NotImplemented
        return results


class FilterInstance(BaseInstance):
    types = Union[FilterType, List[str]]

    def __init__(self, names: types = FilterType.All):
        super().__init__()
        self.names = names

    def filter_data(self, data):
        if self.names == FilterType.All:
            result = data
        elif self.names == FilterType.No:
            result = {}
        elif isinstance(self.names, List):
            result = {}
            for item in self.names:
                result[item] = data[item]
        else:
            raise NotImplemented
        return result
