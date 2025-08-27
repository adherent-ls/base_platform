from typing import List, Union

from ..base_instance import BaseInstance
from ..types.param_type import FilterType, UseField


class InputInstance(BaseInstance):
    types = List[Union[int, UseField]]

    def __init__(self, indices: types = ()):
        super().__init__()
        self.indices = indices

    def extract_data(self, data):
        if isinstance(self.indices, List):
            data_item = []
            for index in self.indices:
                if isinstance(index, int):
                    data_item.append(data[index])
                elif isinstance(index, UseField):
                    data_item.append(index.arg)
                else:
                    raise NotImplemented
        else:
            raise NotImplemented
        return data_item

    @staticmethod
    def data_format(data, indices):
        return [data[index] for index in indices]


class OutputInstance(BaseInstance):
    types = Union[int, List[int]]

    def __init__(self, indices: types = ()):
        super().__init__()
        self.indices = indices

    def update_data(self, result, func_output):
        if isinstance(self.indices, int):
            result[self.indices] = func_output
        elif isinstance(self.indices, List):
            for i, name in enumerate(self.indices):
                result[name] = func_output[i]
        else:
            raise NotImplemented
        return result

    @staticmethod
    def extract_data(data: List, indices: types):
        if indices is None:
            results = data
        elif isinstance(indices, int):
            results = data[indices]
        elif isinstance(indices, List):
            results = []
            for i, index in enumerate(indices):
                results.append(data[index])
        else:
            raise NotImplemented
        return results


class FilterInstance(BaseInstance):
    types = Union[FilterType, List[int]]

    def __init__(self, indices: types = FilterType.All):
        super().__init__()
        self.indices = indices

    def filter_data(self, data):
        if self.indices == FilterType.All:
            result = list(data)
        elif self.indices == FilterType.No:
            result = []
        elif isinstance(self.indices, List):
            result = []
            for item in self.indices:
                result.append(data[item])
        else:
            raise NotImplemented
        return result
