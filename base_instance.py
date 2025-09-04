from typing import Union, Dict, Tuple, List

from .types.base_param_type import UseField, FilterType


class BaseInstance(object):
    def __init__(self):
        super().__init__()


class Condition(BaseInstance):
    def __init__(self, cond):
        super().__init__()
        self.cond = cond

    def __call__(self):
        return self.cond


class ConvertInstance(BaseInstance):
    @staticmethod
    def dict_to_list(data: Dict, names: Union[Tuple, List, str] = None):
        if names is None:
            results = list(data.values())
        elif isinstance(names, str):
            results = data[names]
        elif isinstance(names, List) or isinstance(names, Tuple):
            results = []
            for i, name in enumerate(names):
                if isinstance(name, str):
                    results.append(data[name])
                elif isinstance(name, UseField):
                    results.append(name.arg)
                else:
                    raise NotImplemented
        else:
            raise NotImplemented
        return results

    @staticmethod
    def list_to_dict(data: Union[Tuple, List], names: Union[Tuple, List, str]):
        if names is None:
            names = list(range(len(data)))

        result = {}
        if isinstance(names, str):
            result[names] = data
        elif isinstance(names, List) or isinstance(names, Tuple):
            for i, name in enumerate(names):
                result[name] = data[i]
        else:
            raise NotImplemented
        return result

    @staticmethod
    def dict_update(data: Dict, output: Union[Tuple, List], names: Union[Tuple, List, str]):
        if isinstance(names, str):
            data[names] = output
        elif isinstance(names, List) or isinstance(names, Tuple):
            for i, name in enumerate(names):
                data[name] = output[i]
        else:
            raise NotImplemented
        return data

    @staticmethod
    def list_update(data: List, output: Union[Tuple, List], indices: Union[Tuple, List, int]):
        if isinstance(indices, int):
            data[indices] = output
        elif isinstance(indices, List) or isinstance(indices, Tuple):
            for i, name in enumerate(indices):
                data[name] = output[i]
        else:
            raise NotImplemented
        return data

    @staticmethod
    def dict_extract(data: Dict, names: Union[Tuple, List, FilterType, str]):
        if isinstance(names, str):
            result = data[names]
        elif names == FilterType.All:
            result = data
        elif names == FilterType.No:
            result = {}
        elif isinstance(names, List) or isinstance(names, Tuple):
            result = {}
            for item in names:
                result[item] = data[item]
        else:
            raise NotImplemented
        return result

    @staticmethod
    def list_extract(data: Union[Tuple, List], indices: Union[Tuple, List, FilterType, int]):
        if isinstance(indices, int):
            result = data[indices]
        elif indices == FilterType.All:
            result = list(data)
        elif indices == FilterType.No:
            result = []
        elif isinstance(indices, List) or isinstance(indices, Tuple):
            result = []
            for item in indices:
                result.append(data[item])
        else:
            raise NotImplemented
        return result
