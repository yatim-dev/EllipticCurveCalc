from Model.Curves.Curve import Curve
from Model.Point import Point

class CurveZp(Curve):
    def __init__(self, p: int, a: int, b: int):
        self._p = p
        self._a = a
        self._b = b

    def add(self, first: Point, second: Point) -> Point:
        if first.is_infinity():
            return second
        if second.is_infinity():
            return first

        if first.x == second.x:
            if first.y == 0 or (first.y + second.y) % self._p == 0:
                return Point.infinity()
            # k = (3(x1)^2+a) / (2y1)
            k = (3 * first.x * first.x + self._a) * self._invert(2 * first.y) % self._p
        else:
            # k = (y2 - y1) / (x2 - x1)
            k = (second.y - first.y) * self._invert(second.x - first.x) % self._p

        # x3 = k ^ 2 - x1 - x2
        # y3 = y1 + k(x3 - x1)
        x3 = (k * k - first.x - second.x) % self._p
        y3 = (first.y + k * (x3 - first.x)) % self._p
        return Point(x3, -y3 % self._p)

    def _invert(self, num: int) -> int:
        s, old_s = 0, 1
        r, old_r = self._p, num
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
        return old_s % self._p
