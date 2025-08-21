from typing import Union, List

from base.base_function import BaseFunction


class BaseGraph():
    def __init__(self):
        super().__init__()
        self.modules = {}
        self.owner = None

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def __setattr__(self, name, value):
        if isinstance(value, BaseGraph):
            self.modules[name] = value
        super().__setattr__(name, value)

    def named_children(self):
        for name, module in self.modules.items():
            yield name, module

    def addindent(self, s: str, numSpaces: int) -> str:
        """将多行字符串的除首行外所有行前添加 numSpaces 空格"""
        lines = s.split('\n')
        if len(lines) == 1:
            return s
        first, rest = lines[0], lines[1:]
        rest = [(numSpaces * ' ') + line for line in rest]
        return first + '\n' + '\n'.join(rest)

    def extra_repr(self) -> str:
        # 这里放一些你希望展示的属性
        return f""

    def __repr__(self) -> str:
        # 获取 extra_repr 信息
        extra = self.extra_repr()
        extra_lines = extra.split('\n') if extra else []
        base_indent = 2
        # 遍历子模块，获取 repr 并自动缩进
        child_lines = []
        for name, module in self.named_children():
            mod_str = repr(module)
            # 缩进长度 = len("(<name>): ")
            indent = base_indent + len(f"({name}): ")
            mod_str = self.addindent(mod_str, indent)
            child_lines.append(f"({name}): {mod_str}")

        # 组合所有行：先展示 extra_repr，再展示子模块
        lines = child_lines
        if lines:
            body = "\n".join(" " * base_indent + line for line in lines)
            return f"{self.__class__.__name__}{*extra_lines,}[\n{body}\n]"
        else:
            return f"{self.__class__.__name__}{*extra_lines,}"
