import unittest

from syntaxtree.basic import Expression, WrapperExpression
from syntaxtree.tree import SyntaxTreeNode



class TestBasicExpressions(unittest.TestCase):
    class Expr(Expression):
        yield_type = 'int'
    
    class Expr2(Expression):
        yield_type = 'int'
    
    def test_expression(self):
        'test yield type, expr type and accept'
        expr = self.Expr()
        self.assertEqual(expr.get_yield_type(), 'int')
        self.assertEqual(expr.get_own_type(), self.Expr)
        self.assertEqual(expr.accept(self.Expr), expr)
        self.assertRaises(Exception, expr.accept, self.Expr2)
    
    def test_wrapper_expression(self):
        'test the wrapper expression'
        class Wrapper(WrapperExpression):
            acceptable_type = self.Expr
        
        wrap = Wrapper(self.Expr())
        self.assertEqual(wrap.get_yield_type(), 'int')
        self.assertEqual(wrap.accept(self.Expr), wrap.leaf)
        self.assertRaises(Exception, wrap.accept, self.Expr2)
        
        self.assertRaises(Exception, Wrapper, self.Expr2)



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




