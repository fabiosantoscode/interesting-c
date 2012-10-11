'''
Lexer for interesting-c.
Uses PLY (python-lex-yacc).

The philosophy is to preserve whitespace the best possible, as well as the entire code appearance. C allows for weird syntax and that is beautiful. Also, interesting-c doesn't need to know of any preprocessor tricks.
'''
import unittest

import ply.lex as lex

tokens = [
    'whitespace',
    
    'multiline_comment', 'singleline_comment',
    
    'identifier',
    
    #literals including prefixes and suffixes
    'string_literal',
    'character_literal',
    
    'hexadecimal_number_literal',
    'octal_number_literal',
    'decimal_number_literal',
    
    'hexadecimal_fractional_number_literal',
    'octal_fractional_number_literal',
    'decimal_fractional_number_literal',
    
    #signs and characters
    'equal_sign',
    'plus_sign',
    'minus_sign',
    'times_sign',
    'at_sign',
    'solidus',
    'reverse_solidus',
    'pipe',
    'semicolon',
    'comma',
    'colon',
    'dot',
    'hash',
    'bang',
    'question_mark',
    'and_sign',
    'percent_sign',
    'siphon',
    
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
    'open_square', 'close_square',
]

def t_error(t):
    print 'error:', t

def t_whitespace(t):
    r'[ \t\n]+'
    t.is_newline = '\n' in t.value
    return t

#t_whitespace = r'[ \t\n]+'
# missing: 'multiline_comment', 'singleline_comment'
t_singleline_comment = r'//.*'
t_multiline_comment = r'/\*.*?\*/'
t_identifier = r'[_a-zA-Z][_a-zA-Z0-9]*'



#literals including prefixes and suffixes
t_string_literal = r'".*?(?<=[^\\])("|\\\\")'
    #so far: '".*(?<=[^\\])(?=\\\\"|")(?=")"'
    # it does match "strings \"escaping\" slashes"
    # but doesn't match "strings ending with a slash \\"
    #UPDATE: r'".*?(?<=[^\\])("|\\\\")'
t_character_literal = r"\w?'\w'"
t_hexadecimal_number_literal = r'0[xX][0-9A-Fa-f]+\.[0-9A-Fa-f]+?'
t_octal_number_literal = r'0[0-9]+'
t_decimal_number_literal = r'[0-9]+'

# 'hexadecimal_fractional_number_literal',
# 'octal_fractional_number_literal',
# 'decimal_fractional_number_literal',


#signs and characters
t_equal_sign = r'='
t_plus_sign = r'\+'
t_minus_sign = r'-'
t_times_sign = r'\*'
t_at_sign = r'@'
t_solidus = r'\\'
t_reverse_solidus = r'(/(?=[^/^*])|/$)'
t_pipe = r'\|'
t_semicolon = r';'
t_comma = r','
t_colon = r':'
t_dot = r'\.'
t_hash = r'\#'
t_bang = r'!'
t_question_mark = r'\?'
t_and_sign = r'&'
t_percent_sign = r'%'
t_siphon = r'\$'

# stuff that opens and closes
t_open_paren = r'\('
t_close_paren = r'\)'

t_open_brace = r'{'
t_close_brace = r'}'

t_open_square = r'\['
t_close_square = r'\]'

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



class LexerTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def assertSomeTokens(self, input_string, expected_tokens):
        '''
        test the parser with complex stuff which might contain tokens we don't care about.
        
        '''
        
        tokens = update_and_get_names(input_string)
        
        iter_tokens = iter(tokens)
        matched_tokens = []
        missing_tokens = list(reversed(expected_tokens)) # gonna pop through them
        
        try:
            while not matched_tokens == expected_tokens:
                token = iter_tokens.next()
                if token == missing_tokens[-1]:
                    matched_tokens.append(missing_tokens.pop())
        except IndexError as e:
            err = e
        except StopIteration as e:
            err = e
        except ValueError as e:
            err = e
        else:
            return
        
        self.fail('Error: %s.\nTokens found:   %s\nTokens missing: %s\n' % (repr(err), repr(matched_tokens), repr(missing_tokens)))
        
    def test_everything(self):
        lesslist = []
        
        self.assertTrue(update('     \n    \t'))
        
        self.assertEqual(update('int a=3'), [
            ('identifier', 'int'),
            ('whitespace', ' '),
            ('identifier', 'a'),
            ('equal_sign', '='),
            ('decimal_number_literal', '3')])
        
        self.assertEqual(update('int a=031'), [
            ('identifier', 'int'),
            ('whitespace', ' '),
            ('identifier', 'a'),
            ('equal_sign', '='),
            ('octal_number_literal', '031')])
        
        self.assertEqual(update_and_get_names(
                '{}()?;:.,!*+-/#'), [
            'open_brace', 'close_brace',
            'open_paren', 'close_paren',
            'question_mark',
            'semicolon',
            'colon',
            'dot',
            'comma',
            'bang',
            'times_sign',
            'plus_sign',
            'minus_sign',
            'reverse_solidus',
            'hash'])
        
        self.assertEqual(update_and_get_names('&%<$#>'), [
            'and_sign',
            'percent_sign',
            'open_tag',
            'siphon',
            'hash',
            'close_tag'])
        
        self.assertEqual(update('/*/jugfytgiuh/*/'), [
            ('multiline_comment', '/*/jugfytgiuh/*/')])
        
        self.assertEqual(update('/* */'), [
            ('multiline_comment', '/* */')])
        
        self.assertEqual(update('/**/'), [
            ('multiline_comment', '/**/')])
        
        self.assertEqual(update('/*   /*   /* * */'), [
            ('multiline_comment', '/*   /*   /* * */')])
        
        self.assertEqual(update('/*/*/*/*/*/*/**/asd'), [
            ('multiline_comment', '/*/*/'),
            ('times_sign', '*'),
            ('multiline_comment', '/*/*/'),
            ('times_sign', '*'),
            ('multiline_comment', '/**/'),
            ('identifier', 'asd')])
        
        s = '''
            // And my aunt slew a dragon!
            she is // paper
        '''
    
        self.assertEqual(update_and_get_names(s), [
            'whitespace',
            'singleline_comment',
            'whitespace',
            'identifier',
            'whitespace',
            'identifier',
            'whitespace',
            'singleline_comment',
            'whitespace'])
        
        self.assertEqual(update_and_get_names(' @ '), [
            'whitespace',
            'at_sign',
            'whitespace'])
    
    def test_cut_identifiers(self):
        self.assertEqual(update('id@ntifier'), [
            ('identifier','id'),
            ('at_sign', '@'),
            ('identifier', 'ntifier')])
        
        self.assertEqual(update('id+nti0f-ier'), [
            ('identifier','id'),
            ('plus_sign', '+'),
            ('identifier', 'nti0f'),
            ('minus_sign', '-'),
            ('identifier', 'ier')])
    
    def test_complete_func(self):
        self.assertSomeTokens('''
        int main(){
            return 6;
        }
        ''', [
            'identifier', 'identifier',
            'open_paren', 'close_paren', 'open_brace', 'identifier', 
            'decimal_number_literal', 'semicolon', 'close_brace'])
    
    def test_complete_capsule(self):
        self.assertSomeTokens('''
            abstract capsule Capsule (of pointer to private LinkedListNode<T>)
        ''', [
            'identifier', 'identifier', 'identifier', 'open_paren', 'identifier',
            'open_tag', 'identifier', 'close_tag'
        ])
    
    
if __name__ == '__main__':
    unittest.main()

