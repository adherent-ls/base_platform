import torch

from base.base_instance import BaseInstance
from base.graph.data_graph import SeriesWithNameGraph, UseField, FilterType
from base.instance.config_instance import ConfigInstance


class BaseTrainInstance(BaseInstance):
    def __init__(self, instance: ConfigInstance):
        super().__init__()
        self.instance = instance
        self.pred_graph = SeriesWithNameGraph(
            [
                [lambda data, device: data.to(device), ['image', UseField(instance.device)], 'image'],
                [instance.predictor, ['image'], 'pred'],
            ],
            ['image'],
            'pred'
        )

        self.loss_graph = SeriesWithNameGraph(
            [
                [lambda data, device: data.to(device), ['label', UseField(instance.device)], 'label'],
                [instance.criterion, ['pred', 'label'], 'loss'],
            ],
            ['pred', 'label'],
            'loss'
        )

        self.optim_graph = SeriesWithNameGraph(
            [
                [instance.scheduler.zero_grad, [], []],
                [torch.nn.utils.clip_grad_norm_, [UseField(instance.model.parameters()), UseField(1)], []],
                [lambda loss: loss.backward(), ['loss'], []],
                [instance.scheduler.step, [], []],
                [lambda loss: loss.detach().cpu().numpy(), ['loss'], 'loss', FilterType.No],
            ],
            ['loss'],
            'loss'
        )

        self.metric_graph = SeriesWithNameGraph(
            [
                [lambda data, device: data.to(device), ['label', UseField(instance.device)], 'label'],
                [instance.metric, ['pred', 'label'], 'score', FilterType.No],
            ],
            ['pred', 'label'],
            'score'
        )


class AmpTrainInstance(BaseTrainInstance):
    def __init__(self, instance: ConfigInstance):
        super().__init__(instance)
        self.instance = instance
        from torch import GradScaler
        scaler = GradScaler()  # 初始化梯度缩放器
        self.optim_graph = SeriesWithNameGraph(
            [
                [instance.scheduler.zero_grad, [], []],
                [torch.nn.utils.clip_grad_norm_, [UseField(instance.model.parameters()), UseField(1)], []],
                [lambda loss: scaler.scale(loss).backward(), ['loss'], []],
                [scaler.step, [UseField(instance.scheduler.optimizer)], []],
                [scaler.update, [], []],
                [lambda loss: loss.detach().cpu().numpy(), ['loss'], 'loss', FilterType.No],
            ],
            ['loss'],
            'loss'
        )


class ContrastiveTrainInstance(AmpTrainInstance):
    def __init__(self, instance: ConfigInstance):
        super().__init__(instance)
        self.instance = instance
        self.loss_graph = SeriesWithNameGraph(
            [
                [instance.criterion, ['pred'], 'loss'],
            ],
            ['pred'],
            'loss'
        )
        self.metric_graph = SeriesWithNameGraph(
            [
                [instance.metric, ['pred'], 'score', FilterType.No],
                [lambda score: score.detach().cpu().numpy(), ['score'], 'score'],
            ],
            ['pred'],
            'score'
        )
