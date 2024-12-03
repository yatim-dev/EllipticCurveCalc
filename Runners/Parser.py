from Model.Curves.CurveZp import CurveZp
from Model.Curves.CurveSS import CurveSS
from Model.Curves.CurveNSS import CurveNSS
from Model.Curves.Curve import Curve
from Model.Polynomial import Polynomial
from Runners.Loader import Loader
from typing import Tuple, List, Type, Union


class Parser:
    def __init__(self, lines: enumerate):
        self._lines = lines

    def parse(self) -> Tuple[Curve, List[Loader]]:
        curve_type = self._next_line()
        if curve_type in {'ss', 'nss'}:
            return self._read_gf(curve_type)
        elif curve_type == 'zp':
            return self._read_zp()
        raise ValueError('Неизвестный тип элептической кривой')

    def _read_gf(self, curve_type: str) -> Tuple[Curve, List[Loader]]:
        p = Polynomial.get_irreducible(int(self._next_line()))
        coefficients = [Polynomial(Loader.parse_int(self._next_line())) for _ in range(3)]

        curve = (
            CurveNSS(p, *coefficients) if curve_type == 'nss'
            else CurveSS(p, *coefficients)
        )

        tasks = self._read_tasks(Polynomial)
        return curve, tasks

    def _read_zp(self) -> Tuple[Curve, List[Loader]]:
        p, a, b = (Loader.parse_int(self._next_line()) for _ in range(3))
        curve = CurveZp(p, a, b)
        tasks = self._read_tasks(int)
        return curve, tasks

    def _read_tasks(self, constructor: Union[Type[Polynomial], Type[int]]) -> List[Loader]:
        tasks = []
        while True:
            try:
                task_line = self._next_line()
                tasks.append(Loader.create_task(task_line, constructor))
            except StopIteration:
                break
        return tasks

    def _next_line(self) -> str:
        return next(self._lines)[1].strip().lower()
