class Point:
    _formatters = {
        2: bin, 10: str, 16: hex
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def infinity():
        """Возвращает точку в бесконечости."""
        return Point(None, None)

    def is_infinity(self):
        """Проверка точки"""
        return self.x is None and self.y is None

    def clone(self):
        """Возвращает копию точки"""
        return Point(self.x, self.y)

    def __str__(self):
        return self.format()

    def format(self, base=10):
        """форматирует точки."""
        formatter = self._formatters.get(base, str)
        return 'O' if self.is_infinity() else f'({formatter(self.x)},{formatter(self.y)})'
