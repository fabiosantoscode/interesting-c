import unittest

from parse.lexer import lex, update_and_get_names, update

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
        
    def test_string(self):
        raise unittest.SkipTest
        self.assertEqual(update('"s"     "asd"'), [
            ('string_literal', '"s"'),
            ('string_literal', '"asd"')])
        
        heavily_escaped_string = r'" pls. allow: \"\\\" \\"'
        self.assertEqual(update(heavily_escaped_string), [
            ('string_literal', heavily_escaped_string)])
        
        corner1 = '""""'
        self.assertEqual(update(corner1), [
            ('string_literal', '""'),
            ('string_literal', '""')])
    
    def test_whitespace_behavior(self):
        common_result = [('decimal_number_literal', '3')]
        self.assertEqual(update('3     \n    \t'), common_result)
        self.assertEqual(update('  \n\t \n3\t  '), common_result)
        self.assertEqual(update('  \n  \t \n  3'), common_result)
    
    def test_everything(self):
        self.assertEqual(update('int a=3'), [
            ('identifier', 'int'),
            ('identifier', 'a'),
            ('equal_sign', '='),
            ('decimal_number_literal', '3')])
        
        # self.assertEqual(update('int a=031'), [
        #     ('identifier', 'int'),
        #     ('identifier', 'a'),
        #     ('equal_sign', '='),
        #     ('octal_number_literal', '031')])
        
        self.assertEqual(update_and_get_names(
                '{}()?;:,!*+/'), [
            'open_brace', 'close_brace',
            'open_paren', 'close_paren',
            'question_mark',
            'semicolon',
            'colon',
            'comma',
            'bang',
            'times_sign',
            'plus_sign',
            'reverse_solidus'])
        
        # self.assertEqual(update_and_get_names('&&%<$#>'), [
        #     'and_sign',
        #     'percent_sign',
        #     'less_than_sign',
        #     'siphon',
        #     'hash',
        #     'greater_than_sign'])
    
    def test_comments(self):
        raise unittest.SkipTest
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
            'singleline_comment',
            'identifier',
            'identifier',
            'singleline_comment'])
        
        # self.assertEqual(update_and_get_names(' @ '), ['at_sign'])
    
    def test_cut_identifiers(self):
        self.assertEqual(update('id-ntifier'), [
            ('identifier','id'),
            ('minus_sign', '-'),
            ('identifier', 'ntifier')])
        
        self.assertEqual(update('id+nti0fier'), [
            ('identifier','id'),
            ('plus_sign', '+'),
            ('identifier', 'nti0fier')])
    
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
            'less_than_sign', 'identifier', 'greater_than_sign'
        ])



