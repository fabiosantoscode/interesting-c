from basic import Literal as BaseLiteral

class Literal(BaseLiteral):
    'Literal common functionality'
    
    def __init__(self, value):
        super(Literal, self).__init__(children=[], leaf=value)
    
    value = property(lambda s:s.leaf)
    
    def to_c(self):
        return self.c_value()

class IntLiteral(Literal):
    yield_type = 'int'
    
    def __int__(self):
        return int(self.value)

class DecimalNumberLiteral(IntLiteral):
    def c_value(self):
        return str(int(self.value, 10))

