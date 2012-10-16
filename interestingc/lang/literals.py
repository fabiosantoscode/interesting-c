import lang
from lang import Literal

class _Literal(object):
    'Literal common functionality'
    def to_c(self):
        return self.c_value()
    
    def __init__(self, value):
        self.value = value

class _IntLiteral(_Literal, Literal):
    yield_type = 'int'
    
    def __int__(self):
        return int(self.value)

class DecimalNumberLiteral(_IntLiteral, Literal):
    def c_value(self):
        return str(int(self.value, 10))

