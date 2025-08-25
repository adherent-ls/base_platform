from typing import List


class BaseGraph():
    def __init__(self):
        super().__init__()
        self.modules = {}

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, *args, **kwargs):
        raise NotImplementedError


class SeriesListGraph(BaseGraph):
    def __init__(self, funcs: List[BaseGraph]):
        super().__init__()
        self.funcs = funcs

    def forward(self, *data: any):
        for func in self.funcs:
            data = func(*data)
        return data
