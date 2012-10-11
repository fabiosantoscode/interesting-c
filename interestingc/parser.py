'''
Parser for interesting-c.
Uses PLY (python-lex-yacc).

'''

import unittest

import ply.yacc as yacc

import lexer
import lang
import lang.expressions
import lang.specialexpr
import lang.literals

tokens = lexer.tokens

def p_Expression(p):
    '''Expression : ExpressionEnclosedInParens
                  | And
                  | Or
                  | Not
                  | Term
                  | Multiplication
                  | Division
                  | Sum
                  | Subtraction
                  | Comparison
                  | TernaryExpression
                  | NoExpression'''
    p[0] = p[1].accept(lang.Expression)

def p_NoExpression(p):
    '''NoExpression : '''
    p[0] = lang.specialexpr.NoExpression()

def p_ExpressionEnclosedInParens(p):
    '''ExpressionEnclosedInParens : open_paren Expression close_paren'''
    p[0] = lang.specialexpr.ExpressionEnclosedInParens(p[2])


#unary
def p_Not(p):
    '''Not : bang Expression'''
    p[0] = lang.expressions.NotExpression(p[2])


#binary
def p_Sum(p):
    '''Sum : Expression plus_sign Expression'''
    p[0] = lang.expressions.Sum(p[1], p[3])

def p_Multiplication(p):
    '''Multiplication : Expression times_sign Expression'''
    p[0] = lang.expressions.Multiplication(p[1], p[3])

def p_Subtraction(p):
    '''Subtraction : Expression minus_sign Expression'''
    p[0] = lang.expressions.Subtraction(p[1], p[3])

def p_Division(p):
    '''Division : Expression reverse_solidus Expression'''
    p[0] = lang.expressions.Division(p[1], p[3])

def p_And(p):
    '''And : Expression and_sign and_sign Expression'''
    p[0] = lang.expressions.AndExpression(p[1], p[4])

def p_Or(p):
    '''Or : Expression pipe pipe Expression'''
    p[0] = lang.expressions.OrExpression(p[1], p[4])


#comparisons (binary)
def p_Comparison(p):
    '''Comparison : Expression ComparisonSign Expression'''
    p[0] = lang.expressions.Comparison(p[1], p[3], sign=p[2])

def p_ComparisonSign(p):
    '''ComparisonSign : close_tag
                      | close_tag equal_sign
                      | open_tag
                      | open_tag equal_sign
                      | bang equal_sign
                      | equal_sign equal_sign'''
    p[0] = ''.join(p[1:][:2])
    

#ternary
def p_TernaryExpression(p):
    '''TernaryExpression : Expression question_mark Expression colon Expression'''
    p[0] = lang.expressions.TernaryExpression(p[1], p[3], p[5])


#literals
def p_Literal(p):
    '''Literal : DecimalNumberLiteral '''
    p[0] = p[1].accept(lang.literals.Literal)

def p_Term(p):
    '''Term : Literal
            | Identifier'''
    p[0] = p[1]

def p_Identifier(p):
    '''Identifier : identifier'''
    p[0] = lang.expressions.Identifier(p[1], p.parser.current_module)

def p_DecimalNumberLiteral(p):
    '''DecimalNumberLiteral : decimal_number_literal '''
    p[0] = lang.literals.DecimalNumberLiteral(value=p[1])

yacc.yacc()



def parse_expression(s):
    return yacc.parse(s).accept(lang.Expression)


class ParserTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def assert_expression_equal(self, interesting, c):
        interesting = parse_expression(interesting).to_c()
        self.assertEqual(interesting.replace(' ', ''),
            c.replace(' ', ''))
    
    def test_everything(self):
        print parse_expression('1').to_c()
        # sum
        print parse_expression('2+1').to_c()
        print parse_expression('3+2+1').to_c()

        print parse_expression('(1)').to_c()
        print parse_expression('(2)+1').to_c()
        print parse_expression('(3+2)+1').to_c()
        print parse_expression('3+(2+1)').to_c()
        
        # mixing expressions
        print parse_expression('3*2+1').to_c()
        print parse_expression('3/2*1').to_c()

        print parse_expression('(3*2)+1/2').to_c()
        print parse_expression('3*(2+1)||1').to_c()
        
        # no expression
        print parse_expression('').to_c()
        
        # bool expressions
        print parse_expression('2&&1').to_c()
        print parse_expression('1||2').to_c()
        print parse_expression('!1').to_c()
    
    def test_ternary(self):
        tern = parse_expression('1?2:3').accept(lang.expressions.TernaryExpression)
        
        self.assertEqual(tern.query.value, '1')
        self.assertEqual(tern.if_true.value, '2')
        self.assertEqual(tern.if_false.value, '3')
    
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
        
        from lang.literals import Literal
        
        chain = parse_expression('1<2<3<4').accept(
            lang.expressions.Comparison)
        
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
        
        self.assert_expression_equal('1<2<3<4', '1 < 2 && 2 < 3 && 3 < 4')

if __name__ == '__main__':
    unittest.main()

