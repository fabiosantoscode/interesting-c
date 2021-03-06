import unittest
from syntaxtree import basic, statements, expressions, literals

class StatementTest(unittest.TestCase):
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
    
    def test_declaration(self):
        ident = basic.Identifier('b')
        type_ = basic.Identifier('int')
        decl = statements.Declaration(type_, ident)
        self.assertEqual(decl.type_.name, 'int')
        self.assertEqual(decl.identifier.name, 'b')
