import lang



class ExpressionEnclosedInParens(lang.Expression):
    'Encloses any Expression in parens.'
    def __init__(self, containee):
        self.containee = containee.accept(lang.Expression)
    
    def accept(self, *args):
        return self.containee.accept(*args)
    
    def get_yield_type(self):
        return self.containee.get_yield_type()
    
    def to_c(self):
        return u'(%s)' % self.containee.to_c()



class NoExpression(lang.Expression):
    'No expression at all'
    yield_type = ''
    
    def __init__(self):
        pass
    
    def to_c(self):
        return u''


