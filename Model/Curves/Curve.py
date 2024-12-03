from Model.Point import Point

class Curve:
    def add(self, first: 'Point', second: 'Point'):
        raise NotImplementedError("Add method must be implemented in subclass.")

    def mul(self, first: Point, scalar: int) -> Point:
        result = Point.infinity()
        addend = first
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result
