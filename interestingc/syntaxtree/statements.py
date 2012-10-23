import specialexpr
from basic import Statement, Expression, Identifier



class Assignment(Statement):
    def __init__(self, assignee, expression):
        expression = expression.accept(Expression)
        assignee = assignee.accept(Identifier)
        super(Assignment, self).__init__([assignee, expression], '=')
    expression = property(lambda self: self.children[1])
    assignee = property(lambda self: self.children[0])



class Declaration(Statement):
    def __init__(self, type_, identifier, expression=None):
        identifier = identifier.accept(Identifier)
        if expression is None:
            children = [identifier]
        else:
            assignment = Assignment(identifier, expression)
            children = [identifier, assignment]
        leaf = type_.accept(Identifier)
        super(Declaration, self).__init__(children, leaf)
    
    type_ = property(lambda self:self.leaf)
    identifier = property(lambda self: self.children[0])
    expression = property(lambda self: self.children[1].expression)
    
    def is_assignment(self):
        return len(self.children) == 2



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
    def __init__(self):
        super(EmptyStatement, self).__init__([], 'Empty')



