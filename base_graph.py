from typing import List
from .base_instance import Condition


class BaseGraph():
    def __init__(self):
        super().__init__()
        self.modules = {}

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, *args, **kwargs):
        raise NotImplementedError


class ConditionGraph(BaseGraph):
    def __init__(self, cond: Condition, func_true, func_false):
        super().__init__()
        self.cond = cond
        self.func_true = func_true
        self.func_false = func_false

    def forward(self, *data):
        if self.cond():
            return self.func_true(*data)
        else:
            return self.func_false(*data)


class SeriesListGraph(BaseGraph):
    def __init__(self, funcs: List[BaseGraph]):
        super().__init__()
        self.funcs = funcs

    def forward(self, *data: any):
        for func in self.funcs:
            data = func(*data)
        return data
