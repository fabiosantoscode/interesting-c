from basic import Expression, Statement, Identifier
from statementlist import CodeBlock
from tree import SyntaxTreeNode



class FunctionDefinition(Statement):
    def __init__(self, return_type, name, argumentlist, statements):
        children = [return_type, argumentlist, statements]
        super(FunctionDefinition, self).__init__(children, name)



class TypedArgument(SyntaxTreeNode):
    def __init__(self, type_, name):
        children = [type_, name]
        super(TypedArgument, self).__init__(children, '<Typed Arg>')



class TypedArgumentList(SyntaxTreeNode):
    def __init__(self, arguments):
        children = [arg.accept(TypedArgument) for arg in arguments]
        super(TypedArgumentList, self).__init__(children, '<Args>')

