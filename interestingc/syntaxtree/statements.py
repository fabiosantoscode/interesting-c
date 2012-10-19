import expressions
from basic import Statement



class Assignment(Statement):
    def __init__(self, assignee, expression):
        self.expression = expression.accept(lang.Expression)
        self.assignee = assignee.accept(lang.Identifier)



class ContainerStatement(Statement):
    '''Abstracts an expression from other kinds of statements.'''
    def __init__(self, containee):
        self.containee = containee
    
    def get_own_type(self):
        return self.containee.__class__
    
    def to_c(self):
        return self.containee.to_c()

