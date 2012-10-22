import specialexpr
from basic import Statement, Expression, Identifier



class Assignment(Statement):
    def __init__(self, assignee, expression):
        expression = expression.accept(Expression)
        assignee = assignee.accept(Identifier)
        super(Assignment, self).__init__([assignee, expression], '=')
    expression = property(lambda self: self.children[1])
    assignee = property(lambda self: self.children[0])



class ExpressionStatement(Statement):
    '''Statement which is a lone expression'''
    def __init__(self, containee):
        self.containee = containee
    
    def get_own_type(self):
        return self.containee.__class__
    
    def to_c(self):
        return self.containee.to_c()


class EmptyStatement(Statement):
    ';'
    @property
    def containee(self):
        return specialexpr.NoExpression()



