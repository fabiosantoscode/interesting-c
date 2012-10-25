from syntaxtree.tree import SyntaxTreeNode



class Namespace(object):
    def __init__(self, parent_namespace=None):
        self.parent_namespace = parent_namespace



class CodeBlock(SyntaxTreeNode):
    def __init__(self, statement_list=[], current_namespace=None):
        self.current_namespace = current_namespace
        children = list(statement_list)
        leaf = '{ code block }'
        super(CodeBlock, self).__init__(children, leaf)
