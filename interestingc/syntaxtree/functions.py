from basic import Expression, Statement, Identifier 
from statementlist import StatementList
from tree import SyntaxTreeNode



class FunctionDefinition(Statement):
    def __init__(self, return_type, name, argumentlist, statements):
        argumentlist = argumentlist.accept(TypedArgument)
        children = [return_type, argumentlist, statements]
        super(FunctionDefinition, self).__init__(children, name)



class TypedArgument(SyntaxTreeNode):
    def __init__(self, type_, name):
        children = [
            type_.accept(Identifier),
            name.accept(Identifier)]
        super(TypedArgument, self).__init__(children, '<Typed Arg>')
