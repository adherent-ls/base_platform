class BaseInstance(object):
    def __init__(self):
        super().__init__()


class Condition(BaseInstance):
    def __init__(self, cond):
        super().__init__()
        self.cond = cond

    def __call__(self):
        return self.cond
