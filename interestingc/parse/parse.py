'''
Parser for interesting-c.
Uses PLY (python-lex-yacc).

'''

import ply.yacc as yacc

import lexer
from syntaxtree import basic
from syntaxtree import expressions
from syntaxtree import statements
from syntaxtree import specialexpr
from syntaxtree import literals

tokens = lexer.tokens

precedence = (
    ('right', 'question_mark', 'colon'),
    ('left', 'plus_sign', 'minus_sign'),
    ('left', 'times_sign', 'reverse_solidus'),
    ('left', 'and_sign', 'or_sign'),
    ('nonassoc', 'bang'),
)


def p_Statement(p):
    '''Statement : ExpressionStatement
                 | EmptyStatement
                 | Assignment
                 | Declaration'''
    p[0] = p[1].accept(basic.Statement)

def p_EmptyStatement(p):
    '''EmptyStatement : '''
    p[0] = statements.EmptyStatement()

def p_ExpressionStatement(p):
    '''ExpressionStatement : Expression'''
    p[0] = statements.ExpressionStatement(p[1])

def p_Declaration(p):
    '''Declaration : Identifier whitespace Identifier
                   | Identifier whitespace Identifier equal_sign Expression'''
    type_ = p[1]
    ident = p[3]
    
    if len(p) == 4:
        p[0] = statements.Declaration(type_, ident)
    elif len(p) == 6:
        p[0] = statements.Declaration(type_, ident, p[5])

def p_Assignment(p):
    '''Assignment : Identifier equal_sign Expression'''
    p[0] = statements.Assignment(p[1], p[3])

def p_OptionalExpression(p):
    '''OptionalExpression : Expression
                          | NoExpression'''
    p[0] = p[1].accept(basic.Expression)

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
                  | Minus
                  | Comparison
                  | TernaryExpression'''
    p[0] = p[1].accept(basic.Expression)

def p_NoExpression(p):
    '''NoExpression : '''
    p[0] = specialexpr.NoExpression()

def p_ExpressionEnclosedInParens(p):
    '''ExpressionEnclosedInParens : open_paren Expression close_paren'''
    p[0] = specialexpr.ExpressionEnclosedInParens([p[2]])


#unary
def p_Not(p):
    '''Not : bang Expression'''
    p[0] = expressions.Not(p[2])

def p_Minus(p):
    '''Minus : minus_sign Expression'''
    p[0] = expressions.Minus(p[2])

#binary
def p_Sum(p):
    '''Sum : Expression plus_sign Expression'''
    p[0] = expressions.Sum(p[1], p[3])

def p_Multiplication(p):
    '''Multiplication : Expression times_sign Expression'''
    p[0] = expressions.Multiplication(p[1], p[3])

def p_Subtraction(p):
    '''Subtraction : Expression minus_sign Expression'''
    p[0] = expressions.Subtraction(p[1], p[3])

def p_Division(p):
    '''Division : Expression reverse_solidus Expression'''
    p[0] = expressions.Division(p[1], p[3])

def p_And(p):
    '''And : Expression and_sign Expression'''
    p[0] = expressions.And(p[1], p[3])

def p_Or(p):
    '''Or : Expression or_sign Expression'''
    p[0] = expressions.Or(p[1], p[3])

def p_Comparison(p):
    '''Comparison : Expression ComparisonSign Expression'''
    p[0] = expressions.Comparison(p[1], p[3], sign=p[2])

def p_ComparisonSign(p):
    '''ComparisonSign : less_than_sign
                      | less_than_or_equal_sign
                      | greater_than_sign
                      | greater_than_or_equal_sign
                      | not_equal_sign
                      | double_equal_sign'''
    p[0] = ''.join(p[1:][:2])
    

#ternary
def p_TernaryExpression(p):
    '''TernaryExpression : Expression question_mark Expression colon Expression'''
    p[0] = expressions.TernaryExpression(p[1], p[3], p[5])


#literals
def p_Literal(p):
    '''Literal : DecimalNumberLiteral '''
    p[0] = p[1].accept(literals.Literal)

def p_Term(p):
    '''Term : Literal
            | Identifier'''
    p[0] = p[1]

def p_Identifier(p):
    '''Identifier : identifier'''
    # p[0] = basic.Identifier(p[1], p.parser.current_module)
    p[0] = basic.Identifier(p[1])

def p_DecimalNumberLiteral(p):
    '''DecimalNumberLiteral : decimal_number_literal '''
    p[0] = literals.DecimalNumberLiteral(value=p[1])

yacc.yacc()



def parse_expression(s):
    return yacc.parse(s).containee.accept(basic.Expression)

def parse_statement(s):
    return yacc.parse(s).accept(basic.Statement)
