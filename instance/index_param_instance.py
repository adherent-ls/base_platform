from typing import List, Union

from ..types.param_type import FilterType, UseField

input_types = List[Union[int, UseField]]

output_types = Union[int, List[int]]

filter_types = Union[FilterType, List[int], int]
