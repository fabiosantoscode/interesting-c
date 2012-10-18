
import unittest







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



class SyntaxTreeNodeTest(unittest.TestCase):
    def setUp(self):
        self.testtree = SyntaxTreeNode([
            SyntaxTreeNode([], 'child1'),
            SyntaxTreeNode([], 'child2'),
            SyntaxTreeNode([
                SyntaxTreeNode([], 'grandchild'),
            ], 'child3'),
        ], 'root')
    
    def test_iter(self):
        expectations = ['child1', 'child2', 'child3']
        reality = [child.leaf for child in self.testtree]
        self.assertEqual(expectations, reality)
    

if __name__ == '__main__':
    unittest.main()

