import lang

class Literal(lang.Expression):
    'A literal as an Expression in the parse tree.'
    def __init__(self):
        raise NotImplementedError('lang.expressions.Literal is not '
            'meant to be used directly')

class _Literal(object):
    'Literal common functionality'
    def to_c(self):
        return self.c_value()
    
    def __init__(self, value):
        self.value = value

class _IntLiteral(_Literal):
    yield_type = 'int'
    
    def __int__(self):
        return int(self.value)

class DecimalNumberLiteral(_IntLiteral, Literal):
    def c_value(self):
        return str(int(self.value, 10))

