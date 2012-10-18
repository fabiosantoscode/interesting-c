







class SyntaxTreeNode(object):
    def __init__(self, children=[], leaf=None):
        self.parent = None
        self.children = children
        self.integrate_children()
        self.leaf = leaf
    
    def integrate_children(self):
        for child in self.children:
            child.set_parent(self)
    
    def set_parent(self, parent):
        self.parent = parent
    
    def __iter__(self):
        return iter(self.children)
    
    def add_child(self, child):
        self.down.append(child)


