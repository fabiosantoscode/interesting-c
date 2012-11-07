'''
Lexer for interesting-c.
Uses PLY (python-lex-yacc).

The philosophy is to preserve whitespace the best possible, to avoid
altering the overall code appearance. C allows for weird syntax and
that is beautiful. Also, interesting-c doesn't need to know of any
preprocessor tricks.
'''

import ply.lex as lex

reserved = {
    'return': 'return',
    # 'function': 'function', unused
}

tokens = [
    'whitespace',
    
    # 'multiline_comment', unused
    'singleline_comment',
    
    'identifier',
    
    #literals including prefixes and suffixes
    # 'string_literal', unused
    # 'character_literal', unused
    
    # 'hexadecimal_number_literal', unused
    # 'octal_number_literal', unused
    'decimal_number_literal',
    
    # 'hexadecimal_fractional_number_literal', unused
    # 'octal_fractional_number_literal', unused
    # 'decimal_fractional_number_literal', unused
    
    #signs and characters
    'equal_sign',
    'plus_sign',
    'minus_sign',
    'times_sign',
    # 'at_sign', unused
    # 'solidus', unused
    'reverse_solidus',
    # 'pipe', unused
    'or_sign',
    'semicolon',
    'comma',
    'colon',
    'dot',
    # 'hash', unused
    'bang',
    'question_mark',
    'and_sign',
    # 'ampersand', unused
    # 'percent_sign', unused
    # 'siphon', unused
    
    #comparisons
    'less_than_sign',
    'greater_than_sign',
    'less_than_or_equal_sign',
    'greater_than_or_equal_sign',
    'not_equal_sign',
    'double_equal_sign',
    
    # Open/close
    'open_paren', 'close_paren',
    'open_brace', 'close_brace',
    # 'open_square', 'close_square', unused
] + list(reserved.values())

def t_error(t):
    print 'error:', t

def t_whitespace(t):
    r'[ \t\n\r]+'
    t.is_newline = '\n' in t.value
    return None

# t_singleline_comment = r'//.*'
# t_multiline_comment = r'/\*.*?\*/'
t_identifier = r'[_a-zA-Z][_a-zA-Z0-9]*'



#literals including prefixes and suffixes
# t_string_literal = r'".*?(?<=[^\\])("|\\\\")'
    #so far: '".*(?<=[^\\])(?=\\\\"|")(?=")"'
    # it does match "strings \"escaping\" slashes"
    # but doesn't match "strings ending with a slash \\"
    #UPDATE: r'".*?(?<=[^\\])("|\\\\")'
# t_character_literal = r"\w?'\w'"
# t_hexadecimal_number_literal = r'0[xX][0-9A-Fa-f]+\.[0-9A-Fa-f]+?'
# t_octal_number_literal = r'0[0-9]+'
t_decimal_number_literal = r'[0-9]+'

# 'hexadecimal_fractional_number_literal',
# 'octal_fractional_number_literal',
# 'decimal_fractional_number_literal',


#signs and characters
t_equal_sign = r'='
t_plus_sign = r'\+'
t_minus_sign = r'-'
t_times_sign = r'\*'
# t_at_sign = r'@'
# t_solidus = r'\\'
t_reverse_solidus = r'(/(?=[^/^*])|/$)'
# t_pipe = r'\|'
t_or_sign = r'\|\|'
t_semicolon = r';'
t_comma = r','
t_colon = r':'
t_dot = r'\.'
# t_hash = r'\#'
t_bang = r'!'
t_question_mark = r'\?'
t_and_sign = r'&&'
# t_ampersand = r'&'
# t_percent_sign = r'%'
# t_siphon = r'\$'

# stuff that opens and closes
t_open_paren = r'\('
t_close_paren = r'\)'

t_open_brace = r'{'
t_close_brace = r'}'

# t_open_square = r'\['
# t_close_square = r'\]'

t_less_than_sign = r'<'
t_greater_than_sign = r'>'
t_less_than_or_equal_sign = r'<='
t_greater_than_or_equal_sign = r'>='
t_not_equal_sign = r'!='
t_double_equal_sign = r'=='

lex.lex()



def listlex(lex):
    r = []
    tok = lex.token()
    while tok:
        r.append((tok.type, tok.value))
        tok = lex.token()
    return r

def printlex(input_str):
    for l in update(input_str):
        print '%s: %s' % l

def update(input_str):
    lex.input(input_str)
    lesslist = listlex(lex)
    return lesslist

def update_and_get_names(input_str):
    return [x[0] for x in update(input_str)]

def update_and_get_values(input_str):
    return [x[1] for x in update(input_str)]



