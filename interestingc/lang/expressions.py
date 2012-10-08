import lang

class _Binary(object):
    def __init__(self, left, right):
        'left, right : lang.Expression'
        self.left_operand, self.right_operand = left, right
    
    def render(self):
        return u'%s %s %s' % (self.left_operand.render(), self.sign,
            self.right_operand.render())

class _Unary(object):
    needs_parens = False
    def render(self):
        enclosing = '%s(%s)' if self.needs_parens else '%s%s'
        return enclosing % (self.sign, self.operand.yield_(
            self.yield_type).render())

class ExpressionEnclosedInParens(lang.Expression):
    # Encloses any Expression in parens.
    def __init__(self, containee):
        self.containee = containee.accept(lang.Expression)
    
    def yields(self, *types):
        return self.containee.yields(*types)
    
    def get_yield_types(self):
        return containee.get_yield_types
    
    def yield_(self, type_):
        containee.yield_(type_) # raises the appropriate exception
        return self
    
    def render(self):
        return u'(%s)' % self.containee.render()

class NoExpression(lang.Expression):
    yield_types = {}
    
    def __init__(self):
        pass
    
    def render(self):
        return u''

class Literal(lang.Expression):
    def __init__(self):
        raise NotImplementedError('lang.expressions.Literal is not '
            'meant to be used directly')

class DecimalNumberLiteral(Literal):
    yield_types = ['int', 'bool']
    
    def __init__(self, value):
        self.value = value
    
    def yield_(self, t):
        return self
    
    def render(self):
        return str(self.value)

class Sum(_Binary, lang.Expression):
    sign = '+'

class Subtraction(_Binary, lang.Expression):
    sign = '-'

class Division(_Binary, lang.Expression):
    sign = '/'

class Multiplication(_Binary, lang.Expression):
    sign = '*'

class BooleanExpression(lang.Expression):
    yield_types = {'bool', 'int'}
    
    def __init__(self):
        raise NotImplementedError('lang.expressions.BooleanExpression'
            ' is not meant to be used directly')

class TernaryExpression(lang.Expression):
    def __init__(self, query, if_true, if_false):
        self.query = query
        self.if_true = if_true
        self.if_false = if_false
    
    def get_yield_types(self):
        return if_true.get_yield_types().intersect(if_false.get_yield_types())
    
    def render(self):
        self.enclose_paren()
        return (u'%(query)s ? %(if_true)s : %(if_false)s'
            % self.__dict__)

class NotExpression(_Unary, BooleanExpression):
    sign = '!'

class OrExpression(_Binary, BooleanExpression):
    sign = '||'

class AndExpression(_Binary, BooleanExpression):
    sign = '&&'


