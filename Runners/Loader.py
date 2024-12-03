import re
from Model.Curves import Curve
from Model.Point import Point


class Loader:
    def __init__(self):
        self._operation = None
        self._format = None
        self._first = None
        self._second = None
        self._result = None
        self._base = None

    _formatters = {
        2: bin,
        10: str,
        16: hex
    }

    @property
    def first(self):
        return self._first

    @property
    def second(self):
        return self._second

    @property
    def result(self):
        return self._result

    @staticmethod
    def create_task(line: str, constructor):
        if line.startswith('a'):
            return Loader._parse_add(line, constructor)
        return Loader._parse_mul(line, constructor)

    def calculate(self, curve: Curve):
        if self._operation:
            self._result = self._operation(curve)

    def __str__(self):
        return self._format() if self._format else ""

    @staticmethod
    def _parse_add(task: str, constructor):
        match = re.search(r'\((.*?),(.*?)\) \((.*?),(.*?)\)', task)
        if not match:
            raise ValueError("Неверный формат задания сложения.")
        x1, y1, x2, y2 = map(constructor, map(Loader.parse_int, match.groups()))
        return Loader._initialize_task(
            Point(x1, y1), Point(x2, y2), match.group(1),
            lambda curve, first, second: curve.add(first, second),
            "+"
        )

    @staticmethod
    def _parse_mul(task: str, constructor):
        match = re.search(r'\((.*?),(.*?)\) ([\d\w]+)', task)
        if not match:
            raise ValueError("Неверный формат задания умножения.")
        x1, y1, m = map(Loader.parse_int, match.groups())
        x1, y1 = constructor(x1), constructor(y1)
        return Loader._initialize_task(
            Point(x1, y1), m, match.group(1),
            lambda curve, first, multiplier: curve.mul(first, multiplier),
            "*"
        )

    @staticmethod
    def _initialize_task(first, second, base_value, operation, operator):
        task = Loader()
        task._first = first
        task._second = second
        task._base = Loader.get_base(base_value)
        task._operation = lambda curve: operation(curve, first, second)
        task._format = lambda: ' '.join([
            first.format(task._base), operator,
            Loader._formatters[task._base](second) if isinstance(second, int) else second.format(task._base),
            '=', task.result.format(task._base) if task.result else ""
        ])
        return task

    @staticmethod
    def parse_int(string: str) -> int:
        base = Loader.get_base(string)
        return int(string, base)

    @staticmethod
    def get_base(string: str) -> int:
        string = string.strip()
        if string.startswith('0x'):
            return 16
        if string.startswith('0b'):
            return 2
        return 10
