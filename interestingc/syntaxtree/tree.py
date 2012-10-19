







class SyntaxTreeNode(object):
    def __init__(self, children=[], leaf=None):
        self.parent = None
        self.children = children
        self.integrate_children()
        self.leaf = leaf
    
    def integrate_children(self):
        for child in self:
            child.parent = self
    
    def accept(self, expected):
        if not issubclass(self.__class__, expected):
            raise Exception('Expected %s, instead found %s'
                % (expected, self.__class__.__name__))
        return self
    
    def __iter__(self):
        return iter(self.children)
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def to_c(self):
        raise NotImplementedError


