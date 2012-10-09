import unittest
import lang

class _BooleanExpression(object):
    yield_type = 'bool'

class _Binary(object):
    def __init__(self, left, right):
        'left, right : lang.Expression'
        self.left_operand = left.accept(lang.Expression)
        self.right_operand = right.accept(lang.Expression)
    
    def to_c(self):
        return u'%s %s %s' % (self.left_operand.to_c(), self.sign,
            self.right_operand.to_c())

class _Unary(object):
    needs_parens = False
    
    def __init__(self, operand):
        self.operand = operand.accept(lang.Expression)
    
    def to_c(self):
        enclosing = '%s(%s)' if self.needs_parens else '%s%s'
        return enclosing % (self.sign, self.operand.to_c())

class Sum(_Binary, lang.Expression):
    sign = '+'

class Subtraction(_Binary, lang.Expression):
    sign = '-'

class Division(_Binary, lang.Expression):
    sign = '/'

class Multiplication(_Binary, lang.Expression):
    sign = '*'

class NotExpression(_Unary, _BooleanExpression, lang.Expression):
    sign = '!'

class OrExpression(_Binary, _BooleanExpression, lang.Expression):
    sign = '||'

class AndExpression(_Binary, _BooleanExpression, lang.Expression):
    sign = '&&'

class TernaryExpression(lang.Expression):
    def __init__(self, query, if_true, if_false):
        self.query = query
        self.if_true = if_true.accept(lang.Expression)
        self.yield_type = self.if_true.get_yield_type()
        self.if_false = if_false.accept(lang.Expression, self.yield_type)
    
    def to_c(self):
        return (u'%s ? %s : %s' % self.query.to_c(), self.if_true.to_c(), self.if_false.to_c())

