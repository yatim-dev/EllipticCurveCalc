from Model.Curves.Curve import Curve
from Model.Polynomial import Polynomial
from Model.Point import Point

class CurveSS(Curve):
    def __init__(self, p: 'Polynomial', a: 'Polynomial', b: 'Polynomial', c: 'Polynomial'):
        self._p = p
        self._a = a
        self._b = b
        self._c = c

    def add(self, first: Point, second: Point) -> Point:
        if first.is_infinity():
            return second
        if second.is_infinity():
            return first

        if first.x == second.x:
            if second.y == self._a + first.y:
                return Point.infinity()
            # k = ((x1)^2 + b) / a
            k = (first.x * first.x + self._b) * self._a.invert(self._p) % self._p
        else:
            # k = (y1 + y2) / (x1 + x2)
            k = (first.y + second.y) * (first.x + second.x).invert(self._p) % self._p

        # x3 = k^2 + x1 + x2
        # y3 = y1 + k(x3 + x1)
        x3 = (k * k + first.x + second.x) % self._p
        y3 = (first.y + k * (x3 + first.x)) % self._p
        return Point(x3, (self._a + y3) % self._p)