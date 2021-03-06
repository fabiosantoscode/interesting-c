import unittest
from basic import Expression
import specialexpr

class _BooleanExpression(object):
    yield_type = 'bool'

class _Binary(Expression):
    def __init__(self, left, right, sign=None):
        'left, right : Expression'
        assert self.__class__ != _Binary
        left = left.accept(Expression)
        right = right.accept(Expression)
        sign = sign or self.sign
        super(_Binary, self).__init__([left, right], sign)
    
    left_operand = property( lambda s: s.children[0])
    right_operand = property( lambda s: s.children[1])
    sign = property( lambda s: s.leaf)
    
    def to_c(self):
        return u'%s %s %s' % (self.left_operand.to_c(), self.sign,
            self.right_operand.to_c())

class _Unary(Expression):
    needs_parens = False
    
    def __init__(self, operand, sign=None):
        assert self.__class__ != _Unary
        operand = operand.accept(Expression)
        sign = sign or self.sign
        super(_Unary, self).__init__([operand], sign)
    
    def get_sign(self):
        return self.leaf
    
    def to_c(self):
        enclosing = '%s(%s)' if self.needs_parens else '%s%s'
        return enclosing % (self.get_sign(), self.operand.to_c())



class Sum(_Binary, Expression):
    sign = '+'

class Subtraction(_Binary, Expression):
    sign = '-'

class Division(_Binary, Expression):
    sign = '/'

class Multiplication(_Binary, Expression):
    sign = '*'

class Minus(_Unary, Expression):
    sign = '-'

class Not(_Unary, _BooleanExpression, Expression):
    sign = '!'

class Or(_Binary, _BooleanExpression, Expression):
    sign = '||'

class And(_Binary, _BooleanExpression, Expression):
    sign = '&&'

class TernaryExpression(Expression):
    def __init__(self, query, if_true, if_false):
        query = query
        if_true = if_true.accept(Expression)
        if_false = if_false.accept(Expression)
        super(TernaryExpression, self).__init__([query, if_true, if_false])
    
    query = property(lambda s: s.children[0])
    if_true = property(lambda s: s.children[1])
    if_false = property(lambda s: s.children[2])
    
    def to_c(self):
        children_c = map(Expression.to_c, self.children)
        return (u'%s ? %s : %s' % children_c)



class Comparison(_Binary, Expression):
    'Comparison expressions like <, >= and =='
    yield_type = 'bool'
    signs = ['<', '>', '<=', '>=', '==', '!=']
    
    def has_chain(self):
        return isinstance(self.right_operand, Comparison)
    
    def to_c(self, recursive=False):
        sign = self.sign
        left = self.left_operand.to_c()
        
        if self.has_chain():
            next = self.right_operand.to_c(recursive=True)
            right = self.right_operand.left_operand.to_c()
            return u'%s %s %s && %s' % (left, sign, right, next)
        else:
            right = self.right_operand.to_c()
            return u'%s %s %s' % (left, sign, right)



