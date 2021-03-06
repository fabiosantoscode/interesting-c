from syntaxtree.tree import SyntaxTreeNode
from syntaxtree.namespaces import Namespace


class StatementList(SyntaxTreeNode):
    def __init__(self, statement_list=[]):
        children = list(statement_list)
        leaf = '{ code block }'
        super(StatementList, self).__init__(children, leaf)



class CodeBlock(StatementList):
    def __init__(self, statement_list=[]):
        super(CodeBlock, self).__init__(statement_list)
        
        if self.parent:
            self.namespace = Namespace(
                parent_namespace=self.parent.find_namespace())



class Module(StatementList):
    def __init__(self, statement_list=[]):
        super(Module, self).__init__(statement_list)
        
        self.namespace = Namespace(parent_namespace=None)

