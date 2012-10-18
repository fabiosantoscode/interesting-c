
import unittest
from syntaxtree import SyntaxTreeNode

#class Module(object):

#class ModuleLevels(object):

#class Object(object):
#    '''
#     - Exists
#     - Has supers
#    '''

class Expression(SyntaxTreeNode):
    '''
        Yields a value of a certain type
        There is a type of expression, which is its __class__.
    get_own_type gets __class__, but it can be overridden to fake
    other types and make some expressions transparent.
        Renderable
    '''
    
    def get_yield_type(self):
        return self.yield_type
    
    def get_own_type(self):
        return self.__class__
    
    def accept(self, expected, *ok_types):
        # TODO deprecate ok_types
        if not issubclass(self.__class__, expected):
            raise Exception('Expected %s, instead found %s'
                % (expected, self.__class__.__name__))
        if ok_types:
            if not self.get_yield_type() in ok_types:
                raise Exception('Expected %s' % (', or '.join(
                    ok_types)))
        return self
    
    def to_c(self):
        raise NotImplementedError

class WrapperExpression(Expression):
    containee = property(lambda s: s.leaf)
    acceptable_type = None
    
    def __init__(self, containee):
        if self.acceptable_type is not None:
            containee = containee.accept(self.acceptable_type)
        super(WrapperExpression, self).__init__([], containee)
    
    def get_own_type():
        return self.containee.__class__
    
    def get_yield_type(self):
        return self.containee.get_yield_type()    
    
    def accept(self, *args, **kwargs):
        return self.containee.accept(*args, **kwargs)
    
    def to_c(self, *args, **kwargs):
        return self.containee.to_c(*args, **kwargs)



class Literal(Expression):
    'A literal as an Expression in the parse tree.'



#class Statement(object):
#    '''
#     - Yields nothing
#     - Renderable
#     - Contains expressions
#    '''

class TestLang(unittest.TestCase):
    class Expr(Expression):
        yield_type = 'int'
    
    class Expr2(Expression):
        yield_type = 'int'
    
    def test_expression(self):
        'test yield type, expr type and accept'
        expr = TestLang.Expr()
        self.assertEqual(expr.get_yield_type(), 'int')
        self.assertEqual(expr.get_own_type(), TestLang.Expr)
        self.assertEqual(expr.accept(TestLang), expr)
        self.assertRaises(lambda:expr.accept(Expr2), Exception)
    
    def test_wrapper_expression(self):
        class Wrapper(WrapperExpression):
            acceptable_type = TestLang.Expr
        
        wrap = TestLang.Wrapper(TestLang.Expr)
        self.assertEqual(wrap.get_yield_type(), 'int')
        self.assertEqual(wrap.accept(TestLang.Expr), wrap.leaf)
        self.assertRaises(lambda:wrap.accept(Expr2), Exception)
        
        def try_wrap_something_else():
            TestLang.Wrapper(TestLang.Expr2)
        self.assertRaises(try_wrap_something_else, Exception)

if __name__ == '__main__':
    unittest.main()

