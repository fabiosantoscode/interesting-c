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
from syntaxtree import namespaces
from syntaxtree import functions
from syntaxtree import statementlist

tokens = lexer.tokens

precedence = (
    ('right', 'question_mark', 'colon'),
    ('left', 'plus_sign', 'minus_sign'),
    ('left', 'times_sign', 'reverse_solidus'),
    ('left', 'and_sign', 'or_sign'),
    ('nonassoc', 'bang'),
)

def p_Module(p):
    '''Module : StatementList'''
    p[0] = statementlist.Module(p[1])

def p_ArgumentList(p):
    '''ArgumentList : _ArgumentList'''
    p[0] = functions.ArgumentList(p[1])

def p__ArgumentList(p):
    '''_ArgumentList : Expression
                    | Expression comma ArgumentList
                    |'''
    if len(p) == 4:
        lst = p[3]
    else:
        lst = []
    
    if len(p) > 1:
        lst.append(p[1])
    p[0] = lst

def p_TypedArgumentList(p):
    '''TypedArgumentList : _TypedArgumentList'''
    p[0] = functions.TypedArgumentList(p[1])

def p__TypedArgumentList(p):
    '''_TypedArgumentList : TypedArgument
                         | TypedArgument comma TypedArgumentList
                         | '''
    if len(p) == 4:
        lst = p[3]
    else:
        lst = []
    
    if len(p) > 1:
        lst.append(p[1])
    p[0] = lst
    
def p_TypedArgument(p):
    '''TypedArgument : Identifier Identifier'''
    p[0] = functions.TypedArgument(p[1], p[2])

def p_FunctionDefinition(p):
    '''FunctionDefinition : Identifier Identifier open_paren TypedArgumentList close_paren CodeBlock'''
    p[0] = functions.FunctionDefinition(p[1], p[2], p[4], p[6])

def p_CodeBlock(p):
    '''CodeBlock : open_brace StatementList close_brace'''
    p[0] = statementlist.CodeBlock(p[2])

def p_StatementList(p):
    '''StatementList : Statement
                     | Statement semicolon
                     | Statement semicolon StatementList
                     | '''
    if len(p) == 4:
        lst = p[3]
    else:
        lst = []
    
    if len(p) > 1:
        lst.append(p[1])
    p[0] = lst

def p_Statement(p):
    '''Statement : ExpressionStatement
                 | EmptyStatement
                 | Assignment
                 | Declaration
                 | FunctionDefinition'''
    p[0] = p[1].accept(basic.Statement)

def p_EmptyStatement(p):
    '''EmptyStatement : '''
    p[0] = statements.EmptyStatement()

def p_ExpressionStatement(p):
    '''ExpressionStatement : Expression'''
    p[0] = statements.ExpressionStatement(p[1])

def p_Declaration(p):
    '''Declaration : Identifier Identifier
                   | Identifier Identifier equal_sign Expression'''
    type_ = p[1]
    ident = p[2]
    
    if len(p) == 3:
        p[0] = statements.Declaration(type_, ident)
    elif len(p) == 5:
        p[0] = statements.Declaration(type_, ident, p[4])

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


# unary
def p_Not(p):
    '''Not : bang Expression'''
    p[0] = expressions.Not(p[2])

def p_Minus(p):
    '''Minus : minus_sign Expression'''
    p[0] = expressions.Minus(p[2])

# binary
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
    # actually a n-ary expression but binary from the parser's view
    p[0] = expressions.Comparison(p[1], p[3], sign=p[2])

def p_ComparisonSign(p):
    '''ComparisonSign : less_than_sign
                      | less_than_or_equal_sign
                      | greater_than_sign
                      | greater_than_or_equal_sign
                      | not_equal_sign
                      | double_equal_sign'''
    p[0] = p[1]
    

# the ternary
def p_TernaryExpression(p):
    '''TernaryExpression : Expression question_mark Expression colon Expression'''
    p[0] = expressions.TernaryExpression(p[1], p[3], p[5])


# literals
def p_Literal(p):
    '''Literal : DecimalNumberLiteral '''
    p[0] = p[1].accept(literals.Literal)

def p_DecimalNumberLiteral(p):
    '''DecimalNumberLiteral : decimal_number_literal '''
    p[0] = literals.DecimalNumberLiteral(value=p[1])

# values
def p_Term(p):
    '''Term : Literal
            | Identifier'''
    p[0] = p[1]

def p_Identifier(p):
    '''Identifier : identifier'''
    p[0] = basic.Identifier(p[1])

yacc.yacc()



def parse_statement(s):
    '''parse a statement by parsing a single-statement module
    and extracting the statement. Mainly for tests.'''
    module = yacc.parse('%s;' % s)
    statement = module.children[0]
    return statement

def parse_expression(s):
    statement = parse_statement(s)
    if isinstance(statement, statements.EmptyStatement):
        return specialexpr.NoExpression()
    else:
        return statement.accept(statements.ExpressionStatement
            ).containee

def parse_module(module):
    return yacc.parse(module)
