
import unittest







class SyntaxTreeNode(object):
    def __init__(self, children=[], leaf=None):
        self.parent = None
        self.children = children
        self.leaf = leaf
    
    def set_parent(self, parent):
        self.parent = parent
    
    def add_child(self, child):
        self.down.append(child)



if __name__ == '__main__':
    unittest.main()

