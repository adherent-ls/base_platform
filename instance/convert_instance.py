from typing import List, Dict

import torch

from base.base_function import BaseFunction


class ConvertInstance(BaseFunction):
    model: torch.nn.Module
    output_path: str
    input_names: List
    output_names: List
    dynamic_axes: Dict = None
    opset_version: int = 11
