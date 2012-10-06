'''
Parser for interesting-c.
Uses PLY (python-lex-yacc).

'''

import ply.yacc as yacc
import lexer
import lang
import lang.expressions

tokens = lexer.tokens

def p_Expression(p):
    '''Expression : DecimalNumberLiteral
                  | Sum'''
    p[0] = p[1].accept(lang.Expression)

def p_Sum(p):
    '''Sum : Expression plus_sign Expression'''
    expr = p[1].accept(lang.Expression)
    term = p[3].accept(lang.Expression)
    p[0] = expressions.Sum()

def p_Literal(p):
    '''Literal : DecimalNumberLiteral '''

"""
def p_Term(p):
    '''Term : Literal
            | Identifier'''
    p[0] = p[1]

def p_Identifier(p):
    '''Identifier : identifier'''
"""

def p_DecimalNumberLiteral(p):
    '''DecimalNumberLiteral : decimal_number_literal '''
    p[0] = lang.expressions.DecimalNumberLiteral(value=p[1])

yacc.yacc()



def parse_expression(s):
    return yacc.parse(s).accept(lang.Expression)

if __name__ == '__main__':
    print parse_expression('1').render()
    print parse_expression('2+1').render()
    print parse_expression('3+2+1').render()


