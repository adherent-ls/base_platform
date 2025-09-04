from typing import List, Union

from .base_param_type import FilterType, UseField

input_types = List[Union[str, UseField]]

output_types = Union[str, List[str]]

filter_types = Union[FilterType, List[str], str]
