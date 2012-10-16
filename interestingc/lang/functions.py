from expressions import Expression

class ArgumentList(list):
    pass

class FunctionCall(Expression):
    def __init__(self, callee, argumentlist):
        self.callee = callee
        self.argumentlist = argumentlist


