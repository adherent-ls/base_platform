from typing import Optional, Callable

import torch

from base.base_function import BaseFunction


class TorchFunction(torch.nn.Module, BaseFunction):
    def __init__(self):
        super().__init__()


class OptimizerFunction(BaseFunction):
    def __init__(self, optimizer):
        super().__init__()
        self.optimizer = optimizer

    def zero_grad(self, set_to_none: bool = True):
        self.optimizer.zero_grad(set_to_none)

    def step(self, closure: Optional[Callable[[], float]] = None):
        self.optimizer.step(closure)

    def adjust_learning_rate(self, epoch):
        pass


class LossFunction(BaseFunction):
    def __init__(self):
        super().__init__()

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def backward(self, loss):
        res = loss.backward()
        return res


class MetricFunction(BaseFunction):
    pass
