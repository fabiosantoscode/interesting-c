import unittest

from syntaxtree.basic import Expression, WrapperExpression
from syntaxtree.tree import SyntaxTreeNode



class SyntaxTreeNodeTest(unittest.TestCase):
    def setUp(self):
        self.testtree = SyntaxTreeNode([
            SyntaxTreeNode([], 'child1'),
            SyntaxTreeNode([], 'child2'),
            SyntaxTreeNode([
                SyntaxTreeNode([], 'grandchild'),
            ], 'child3'),
        ], 'root')
    
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
