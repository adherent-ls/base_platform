from typing import List, Union, Any

from ..base_graph import BaseGraph
from .base_param_type import FilterType, UseField

graph_types = Union[BaseGraph, Any]

input_types = List[Union[str, UseField]]

output_types = Union[str, List[str]]

filter_types = Union[FilterType, List[str], str]
