'''
Parser for interesting-c.
Uses PLY (python-lex-yacc).

'''

import unittest

import ply.yacc as yacc

import lexer
import lang
import lang.expressions

tokens = lexer.tokens

def p_Expression(p):
    '''Expression : Literal
                  | Multiplication
                  | Division
                  | Sum
                  | Subtraction
                  | And
                  | Or
                  | Not
                  | TernaryExpression
                  | ExpressionEnclosedInParens
                  | NoExpression'''
    p[0] = p[1]

def p_NoExpression(p):
    '''NoExpression : '''
    p[0] = lang.expressions.NoExpression()

def p_ExpressionEnclosedInParens(p):
    '''ExpressionEnclosedInParens : open_paren Expression close_paren'''
    p[0] = lang.expressions.ExpressionEnclosedInParens(p[2])

#unary
def p_Not(p):
    '''Not : bang Expression'''
    p[0] = lang.Expressions.NotExpression(p[2])

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

#ternary
def p_TernaryExpression(p):
    '''TernaryExpression : Expression question_mark Expression colon Expression'''
    p[0] = lang.expressions.TernaryExpression(p[1], p[3], p[5])

#n'ary
def p_ChainedComparison(p):
    pass

#literals
def p_Literal(p):
    '''Literal : DecimalNumberLiteral '''
    p[0] = p[1].accept(lang.expressions.Literal)

def p_Term(p):
    '''Term : Literal
            | Identifier'''
    p[0] = p[1]

def p_Identifier(p):
    '''Identifier : identifier'''
    p[0] = lang.expressions.Identifier(p[1], p.parser.current_module)

def p_DecimalNumberLiteral(p):
    '''DecimalNumberLiteral : decimal_number_literal '''
    p[0] = lang.expressions.DecimalNumberLiteral(value=p[1])

yacc.yacc()



def parse_expression(s):
    return yacc.parse(s).accept(lang.Expression)


class ParserTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def assert_expression_equal(self, test, s):
        s = parse_expression(s).render()
        self.assertEqual(s.replace(' ', ''), test.replace(' ', ''))
    
    def assert_expression_python_equal(self, s, test):
        self.assertEqual(eval(s), test(s))
    
    def test_everything(self):
        print parse_expression('1').render()
        # sum
        print parse_expression('2+1').render()
        print parse_expression('3+2+1').render()

        print parse_expression('(1)').render()
        print parse_expression('(2)+1').render()
        print parse_expression('(3+2)+1').render()
        print parse_expression('3+(2+1)').render()
        
        # mixing expressions
        print parse_expression('2&&1').render()
        print parse_expression('3*2+1').render()
        print parse_expression('3/2*1').render()

        print parse_expression('(3*2)+1/2').render()
        print parse_expression('3*(2+1)||1').render()
        
        # no expression
        print parse_expression('').render()
    
    def test_ternary(self):
        tern = parse_expression('1?2:3').accept(lang.expressions.TernaryExpression)
    
if __name__ == '__main__':
    unittest.main()

