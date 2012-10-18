from basic import Expression


class ExpressionEnclosedInParens(Expression):
    'Encloses any Expression in parens.'
    containee = property(lambda s: s.children[0])
    
    def accept(self, *args):
        return self.containee.accept(*args)
    
    def get_yield_type(self):
        return self.containee.get_yield_type()
    
    def to_c(self):
        return u'(%s)' % self.containee.to_c()



class NoExpression(Expression):
    'No expression at all'
    yield_type = ''
    
    def __init__(self):
        super(NoExpression, self).__init__([])
    
    def to_c(self):
        return u''



