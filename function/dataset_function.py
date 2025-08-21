from torch.utils.data import Dataset

from base.base_function import BaseFunction


class DatasetFunction(Dataset, BaseFunction):
    def __init__(self):
        super().__init__()
