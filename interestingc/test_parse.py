import unittest

from parse import parse_expression
import lang



class ParserTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_ternary(self):
        tern = parse_expression('1?2:3').accept(
            lang.expressions.TernaryExpression)
        
        self.assertEqual(tern.query.value, '1')
        self.assertEqual(tern.if_true.value, '2')
        self.assertEqual(tern.if_false.value, '3')
        
        self.assertIsInstance(parse_expression('1?2:3*1').if_false,
        lang.expressions.Multiplication)
    
    def test_cmp(self):
        cmp_ = parse_expression('1<2').accept(
            lang.expressions.Comparison)
        
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
            lang.expressions.Comparison)
        
        self.assertTrue(isinstance(chain.left_operand, lang.Literal))
        self.assertFalse(isinstance(chain.right_operand, lang.Literal)
            )
        
        r = chain.right_operand
        
        self.assertTrue(isinstance(r.left_operand, lang.Literal))
        self.assertFalse(isinstance(r.right_operand, lang.Literal))
        self.assertEqual(r.left_operand.value, '2')
        
        rr = chain.right_operand.right_operand
        
        self.assertTrue(isinstance(rr.left_operand, lang.Literal))
        self.assertTrue(isinstance(rr.right_operand, lang.Literal))
        self.assertEqual(rr.left_operand.value, '3')
        self.assertEqual(rr.right_operand.value, '4')
    
    def test_precedence(self):
        calculation = parse_expression('1*2+3')
        #assert left side is expression, and thus is calculated first
        self.assertIsInstance(calculation.left_operand, lang.expressions.Multiplication)
        self.assertEqual(calculation.right_operand.value, '3')
        
        calculation = parse_expression('1-2/3')
        #assert right side is expression, and thus is calculated first
        self.assertIsInstance(calculation.right_operand, lang.expressions.Division)
        self.assertIsInstance(calculation.left_operand, lang.Literal)
        
    def test_unary_minus(self):
        calculation = parse_expression('1*-(1)')
        self.assertIsInstance(calculation.left_operand, lang.Literal)
        self.assertIsInstance(calculation.right_operand, lang.expressions.Minus)
        calculation = parse_expression('1*-1')
        self.assertIsInstance(calculation.right_operand, lang.expressions.Minus)
        
        self.assertIsInstance(parse_expression('-1'),
             lang.expressions.Minus)
        
    
    def test_precedence_with_parens(self):
        calculation = parse_expression('(1*2)+3')
        
        #assert that parens make the left side an expression
        self.assertIsInstance(calculation.right_operand, lang.Literal)
        self.assertIsInstance(calculation.left_operand, lang.expressions.Multiplication)
    
    def test_noexpression(self):
        noexp = parse_expression('')
        self.assertIsInstance(noexp, lang.specialexpr.NoExpression)
    
    def test_bool_arithmetic(self):
        or_ = parse_expression('1||1')
        and_ = parse_expression('1&&1')
        not_ = parse_expression('!1')
        
        self.assertIsInstance(or_, lang.expressions.Or)
        self.assertIsInstance(and_, lang.expressions.And)
        self.assertIsInstance(not_, lang.expressions.Not)
    
    def test_bool_arithmetic_precedence(self):
        complex_ = parse_expression('1&&1||0')
        self.assertIsInstance(complex_, lang.expressions.Or)
        
        complex_ = parse_expression('1||0&&1')
        self.assertIsInstance(complex_, lang.expressions.And)
        
        complex_ = parse_expression('1&&(1||0)')
        self.assertIsInstance(complex_, lang.expressions.And)
        
        complex_ = parse_expression('1||(0&&1)')
        self.assertIsInstance(complex_, lang.expressions.Or)



if __name__ == '__main__':
    unittest.main()
