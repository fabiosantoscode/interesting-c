import lang
from lang import Literal

class _Literal(Literal):
    'Literal common functionality'
    
    def __init__(self, value):
        super(_Literal, self).__init__(children=[], leaf=value)
    
    value = property(lambda s:s.leaf)
    
    def to_c(self):
        return self.c_value()

class _IntLiteral(_Literal):
    yield_type = 'int'
    
    def __int__(self):
        return int(self.value)

class DecimalNumberLiteral(_IntLiteral):
    def c_value(self):
        return str(int(self.value, 10))

