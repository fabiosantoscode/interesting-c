import unittest

from syntaxtree.basic import Expression, WrapperExpression
from syntaxtree.tree import SyntaxTreeNode



class SyntaxTreeNodeTest(unittest.TestCase):
    def setUp(self):
        self.child1 = SyntaxTreeNode([], 'child1')
        self.child2 = SyntaxTreeNode([], 'child2')
        self.grandchild = SyntaxTreeNode([], 'grandchild')
        self.child3 = SyntaxTreeNode([self.grandchild], 'child3')
        self.testtree = SyntaxTreeNode([self.child1, self.child2,
            self.child3], 'root')
    
    def test_traverse(self):
        self.assertEqual(self.child1.get_parent(), self.testtree)
        self.assertEqual(self.grandchild.get_parent(), self.child3)
        self.assertRaises(Exception, self.testtree.get_parent)
        
        self.assertEqual(self.child2.get_next(), self.child3)
        self.assertRaises(IndexError, self.child3.get_next)
        self.assertEqual(self.child2.get_previous(), self.child1)
        self.assertRaises(IndexError, self.child1.get_previous)
        
        self.assertEqual(self.grandchild.get_all_in_level(),
            [self.grandchild])
        self.assertEqual(self.child2.get_all_in_level(),
            [self.child1, self.child2, self.child3])
        self.assertEqual(self.child3.get_silblings(),
            [self.child1, self.child2])
        
        self.assertEqual(list(self.grandchild.ancestors()),
            [self.child3, self.testtree])
        
        self.assertEqual(self.grandchild.get_ancestor(lambda anc: anc is self.child3), self.child3)
    
    def test_accept(self):
        class Expr(SyntaxTreeNode): pass
        class Expr2(SyntaxTreeNode): pass
        
        expr = Expr()
        self.assertEqual(expr.accept(Expr), expr)
        self.assertEqual(expr.accept(object), expr)
        self.assertEqual(expr.accept(SyntaxTreeNode), expr)
        self.assertRaises(Exception, expr.accept, Expr2)
    
    def test_iter(self):
        expectations = ['child1', 'child2', 'child3']
        reality = [child.leaf for child in self.testtree]
        self.assertEqual(expectations, reality)
    
    def test_children_integration(self):
        self.assertEqual([c.parent for c in self.testtree],
            [self.testtree] * 3)
        
        self.assertEqual(self.testtree.children[2].children[0].parent,
            self.testtree.children[2])
    
    def test_add_child(self):
        self.testtree.add_child(SyntaxTreeNode)
        self.assertEqual(len(self.testtree.children), 4)
        self.assertEqual(self.testtree.children[-1].parent, self.testtree)
