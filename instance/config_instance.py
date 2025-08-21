from typing import Union, Callable, List

import torch

from base.base_function import BaseFunction
from base.base_graph import BaseGraph
from base.function.torch_function import TorchFunction, LossFunction, MetricFunction, OptimizerFunction


class ConfigInstance(BaseFunction):
    exp_name: str
    show_step: int
    save_step: int
    save_root: str
    is_train_valid: bool = False
    inference_epoch: int = -1
    batch_size: int = 4

    data: dict
    model: Union[BaseGraph, TorchFunction, torch.nn.Module]
    scheduler: Union[BaseGraph, OptimizerFunction, torch.optim.Optimizer]
    criterion: Union[BaseGraph, LossFunction, torch.nn.modules.loss._Loss]
    metric: Union[BaseGraph, MetricFunction, Callable]
    predictor: Union[BaseGraph, TorchFunction, torch.nn.Module]
    saver: BaseGraph
    writer: any

    device: Union[str, List[str]] = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    epoch: int = 1000
    start_step: int = 0
    best_score: float = None

    def to(self, device):
        raise NotImplementedError

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()


class DiffusionInstance(ConfigInstance):
    valid_limit: int = 0
