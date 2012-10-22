import unittest
from syntaxtree import basic, statements, expressions, literals

class TestStatements(unittest.TestCase):
    def test_expression_statement(self):
        expr = basic.Expression()
        exprstatement = statements.ExpressionStatement(expr)
        self.assertEqual(exprstatement.containee, expr)
    
    def test_nostatement(self):
        nostatement = statements.EmptyStatement()
        self.assertEqual(nostatement.children, [])
    
    def test_assignment(self):
        ident = basic.Identifier('a')
        expr = literals.DecimalNumberLiteral('45')
        assignment = statements.Assignment(expression=expr, 
            assignee=ident)
