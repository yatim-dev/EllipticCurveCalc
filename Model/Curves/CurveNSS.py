from Model.Curves.Curve import Curve
from Model.Polynomial import Polynomial
from Model.Point import Point

class CurveNSS(Curve):
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
            if second.y == self._a * first.x + first.y:
                return Point.infinity()
            # k = ((x1)^2 + ay1) / ax1
            k = (first.x * first.x + self._a * first.y) * (self._a * first.x).invert(self._p) % self._p
        else:
            # k = (y1 + y2) / (x1 + x2)
            k = (first.y + second.y) * (first.x + second.x).invert(self._p) % self._p

        # x3 = k*2 + ak + b + x1 + x2
        # y3 = kx3+d = k(x3+x1) + y1
        x3 = (k * k + self._a * k + self._b + first.x + second.x) % self._p
        y3 = (first.y + k * (x3 + first.x)) % self._p
        return Point(x3, (self._a * x3 + y3) % self._p)