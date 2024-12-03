import re


class Polynomial:
    _irreducible = {
        2: 'x^2+x+1', 3: 'x^3+x+1', 4: 'x^4+x+1', 5: 'x^5+x^2+1',
        6: 'x^6+x+1', 7: 'x^7+x^3+1', 8: 'x^8+x^4+x^3+x^2+1', 9: 'x^9+x^4+1',
        10: 'x^10+x^3+1', 11: 'x^11+x^2+1', 12: 'x^12+x^6+x^4+x+1',
        13: 'x^13+x^4+x^3+x+1', 14: 'x^14+x^10+x^6+x+1', 15: 'x^15+x+1',
        16: 'x^16+x^12+x^3+x+1', 17: 'x^17+x^3+1', 18: 'x^18+x^7+1',
        19: 'x^19+x^5+x^2+x+1', 20: 'x^20+x^3+1', 21: 'x^21+x^2+1',
        22: 'x^22+x+1', 23: 'x^23+x^5+1', 24: 'x^24+x^7+x^2+x+1',
        25: 'x^25+x^3+1', 26: 'x^26+x^6+x^2+x+1', 27: 'x^27+x^5+x^2+x+1',
        28: 'x^28+x^3+1', 29: 'x^29+x^2+1', 30: 'x^30+x^23+x^2+x+1',
        31: 'x^31+x^3+1', 32: 'x^32+x^22+x^2+x+1', 36: 'x^36+x^11+1',
        40: 'x^40+x^9+x^3+x+1', 48: 'x^48+x^28+x^3+x+1',
        56: 'x^56+x^42+x^2+x+1', 64: 'x^64+x^46+x^4+x+1',
        72: 'x^72+x^62+x^3+x^2+1', 80: 'x^80+x^54+x^2+x+1',
        96: 'x^96+x^31+x^4+x+1', 128: 'x^128+x^7+x^2+x+1',
        160: 'x^160+x^19+x^4+x+1', 163: 'x^163+x^7+x^6+x^3+1',
        192: 'x^192+x^107+x^4+x+1', 233: 'x^233+x^74+1',
        256: 'x^256+x^16+x^3+x+1', 283: 'x^283+x^12+x^7+x^5+1',
        409: 'x^409+x^87+1', 571: 'x^571+x^10+x^5+x^2+1'
    }

    def __init__(self, bits: int):
        self._bits = bits

    def __str__(self):
        return bin(self._bits)

    def __index__(self):
        return self._bits

    @property
    def bits(self):
        return self._bits

    @staticmethod
    def get_irreducible(n: int) -> 'Polynomial':
        if n not in Polynomial._irreducible:
            raise ValueError(f"Irreducible polynomial for degree {n} not found.")
        return Polynomial.parse_polynomial(Polynomial._irreducible[n])

    @staticmethod
    def parse_polynomial(string: str) -> 'Polynomial':
        result = 0
        monomials = re.findall(r'(\d*)x\^(\d+)|x\^(\d+)|(\d*)x|1', string)
        for factor, exponent1, exponent2, single_x in monomials:
            exponent = int(exponent1 or exponent2 or (1 if single_x else 0))
            result |= 1 << exponent
        return Polynomial(result)

    def clone(self) -> 'Polynomial':
        return Polynomial(self._bits)

    def __eq__(self, other: 'Polynomial') -> bool:
        return self._bits == other._bits

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        return Polynomial(self._bits ^ other._bits)

    def __len__(self):
        return self._bits.bit_length()

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        result = 0
        addend_bits = self._bits
        other_bits = other._bits
        while other_bits:
            if other_bits & 1:
                result ^= addend_bits
            addend_bits <<= 1
            other_bits >>= 1
        return Polynomial(result)

    def __mod__(self, other: 'Polynomial') -> 'Polynomial':
        result = self._bits
        while result.bit_length() >= other._bits.bit_length():
            shift = result.bit_length() - other._bits.bit_length()
            result ^= other._bits << shift
        return Polynomial(result)

    def __lshift__(self, shift: int) -> 'Polynomial':
        return Polynomial(self._bits << shift)

    def __rshift__(self, shift: int) -> 'Polynomial':
        return Polynomial(self._bits >> shift)

    def _polydiv(self, divisor: 'Polynomial') -> 'Polynomial':
        quotient, remainder = 0, self._bits
        divisor_bits = divisor._bits
        while remainder.bit_length() >= divisor_bits.bit_length():
            shift = remainder.bit_length() - divisor_bits.bit_length()
            quotient ^= 1 << shift
            remainder ^= divisor_bits << shift
        return Polynomial(quotient)

    def invert(self, p: 'Polynomial') -> 'Polynomial':
        old_r, r = p, self.clone()
        old_t, t = Polynomial(0), Polynomial(1)
        while r != Polynomial(0):
            quotient = old_r._polydiv(r)
            old_r, r = r, old_r + quotient * r
            old_t, t = t, old_t + quotient * t
        if old_r._bits != 1:
            raise ArithmeticError("No inverse exists.")
        return old_t % p
