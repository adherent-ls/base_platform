import numpy as np

from base.base_function import BaseFunction


class NumpyFunction(BaseFunction):

    def __init__(self):
        super().__init__()


# Variable
class OpencvFunction(NumpyFunction):
    def __init__(self):
        super().__init__()

    def __call__(self, *data):
        return self.forward(*data)

    def forward(self, *args, **kwargs) -> np.ndarray:
        raise NotImplementedError


class ImageFunction(OpencvFunction):
    def __init__(self):
        super().__init__()

    def forward(self, images) -> np.ndarray:
        raise NotImplementedError


class TextFunction(OpencvFunction):
    def __init__(self):
        super().__init__()

    def __call__(self, images, labels, *args, **kwargs):
        labels = self.forward(labels)
        return images, labels, args, kwargs

    def forward(self, labels) -> np.ndarray:
        raise NotImplementedError


class AugmentFunction(OpencvFunction):
    def __init__(self):
        super().__init__()

    def __call__(self, *data):
        return self.forward(*data)

    def forward(self, *data) -> np.ndarray:
        raise NotImplementedError
