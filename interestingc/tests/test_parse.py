import unittest

from parse.parse import parse_expression, parse_statement
from syntaxtree.basic import Literal
from syntaxtree import expressions
from syntaxtree import specialexpr
from syntaxtree import statements
from syntaxtree.namespaces import Namespace


class ParserTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_tolerate_whitespace(self):
        s1 = parse_statement('int a = 3')
        self.assertIsInstance(s1, statements.Declaration)
        s2 = parse_statement('b =    \n\t6\r')
        self.assertIsInstance(s2, statements.Assignment)
        e1 = parse_expression('a   +      5     +     9')
        self.assertIsInstance(e1, expressions.Sum)
        e2 = parse_expression('-   4')
        self.assertIsInstance(e2, expressions.Minus)
    
    def test_variable_declaration(self):
        decl = parse_statement('int a').accept(statements.Declaration)
        assdecl = parse_statement('int a=3').accept(statements.Declaration)
        self.assertEqual(decl.identifier.name, 'a')
        self.assertEqual(decl.type_.name, 'int')
        self.assertEqual(assdecl.identifier.name, 'a')
        self.assertEqual(assdecl.type_.name, 'int')
        self.assertEqual(assdecl.expression.value, '3')
    
    def test_assignment(self):
        ass = parse_statement('a=3').accept(statements.Assignment)
        self.assertEqual(ass.assignee.name, 'a')
        self.assertEqual(ass.expression.value, '3')
    
    def test_ternary(self):
        tern = parse_expression('1?2:3').accept(
            expressions.TernaryExpression)
        
        self.assertEqual(tern.query.value, '1')
        self.assertEqual(tern.if_true.value, '2')
        self.assertEqual(tern.if_false.value, '3')
        
        self.assertIsInstance(parse_expression('1?2:3*1').if_false,
            expressions.Multiplication)
    
    def test_cmp(self):
        cmp_ = parse_expression('1<2').accept(
            expressions.Comparison)
        
        self.assertEqual(cmp_.left_operand.value, '1')
        self.assertEqual(cmp_.right_operand.value, '2')
        self.assertEqual(cmp_.sign, '<')
    
    def test_chain_cmp(self):
        'test chain comparisons'
        
        '''
        The difference between a plain comparison and a chain
        comparison is that a regular comparison is binary, while the
        chain comparison is n-ary
        
        expression:
            1 < 2 < 3
        would yield false, because it would evaluate to:
            1 < (2 < 3)
        and then
            1 < (true)
        '''
        
        chain = parse_expression('1<2<3<4').accept(
            expressions.Comparison)
        
        self.assertTrue(isinstance(chain.left_operand, Literal))
        self.assertFalse(isinstance(chain.right_operand, Literal))
        
        r = chain.right_operand
        
        self.assertTrue(isinstance(r.left_operand, Literal))
        self.assertFalse(isinstance(r.right_operand, Literal))
        self.assertEqual(r.left_operand.value, '2')
        
        rr = chain.right_operand.right_operand
        
        self.assertTrue(isinstance(rr.left_operand, Literal))
        self.assertTrue(isinstance(rr.right_operand, Literal))
        self.assertEqual(rr.left_operand.value, '3')
        self.assertEqual(rr.right_operand.value, '4')
    
    def test_precedence(self):
        calculation = parse_expression('1*2+3')
        #assert left side is expression, and thus is calculated first
        self.assertIsInstance(calculation.left_operand, expressions.Multiplication)
        self.assertEqual(calculation.right_operand.value, '3')
        
        calc = parse_expression('1-2/3')
        #assert right side is expression, and thus is calculated first
        self.assertIsInstance(calc, expressions.Subtraction)
        self.assertIsInstance(calc.right_operand, expressions.Division)
        self.assertIsInstance(calc.left_operand, Literal)
        
    def test_unary_minus(self):
        calculation = parse_expression('1*-(1)')
        self.assertIsInstance(calculation.left_operand, Literal)
        self.assertIsInstance(calculation.right_operand, expressions.Minus)
        calculation = parse_expression('1*-1')
        self.assertIsInstance(calculation.right_operand, expressions.Minus)
        
        self.assertIsInstance(parse_expression('-1'),
             expressions.Minus)
    
    def test_precedence_with_parens(self):
        calculation = parse_expression('(1*2)+3')
        
        #assert that parens make the left side an expression
        self.assertIsInstance(calculation.right_operand, Literal)
        self.assertIsInstance(calculation.left_operand, expressions.Multiplication)
    
    def test_noexpression(self):
        noexp = parse_expression('')
        self.assertIsInstance(noexp, specialexpr.NoExpression)
    
    def test_bool_arithmetic(self):
        or_ = parse_expression('1||1')
        and_ = parse_expression('1&&1')
        not_ = parse_expression('!1')
        
        self.assertIsInstance(or_, expressions.Or)
        self.assertIsInstance(and_, expressions.And)
        self.assertIsInstance(not_, expressions.Not)
    
    def test_bool_arithmetic_precedence(self):
        complex_ = parse_expression('1&&1||0')
        self.assertIsInstance(complex_, expressions.Or)
        
        complex_ = parse_expression('1||0&&1')
        self.assertIsInstance(complex_, expressions.And)
        
        complex_ = parse_expression('1&&(1||0)')
        self.assertIsInstance(complex_, expressions.And)
        
        complex_ = parse_expression('1||(0&&1)')
        self.assertIsInstance(complex_, expressions.Or)


