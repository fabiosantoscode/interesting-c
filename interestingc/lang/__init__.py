
#class Module(object):

#class ModuleLevels(object):

#class Object(object):
#    '''
#     - Exists
#     - Has supers
#    '''

from syntaxtree import SyntaxTreeNode

class Expression(SyntaxTreeNode):
    '''
        Yields a value of a certain type
        There is a type of expression, which is its __class__.
    get_own_type gets __class__, but it can be overridden to fake
    other types and reduce complexity.
        Renderable
    '''
    
    def get_yield_type(self):
        return self.yield_type
    
    def get_own_type(self):
        return self.__class__
    
    def accept(self, expected, *ok_types):
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



class Literal(Expression):
    'A literal as an Expression in the parse tree.'



#class Statement(object):
#    '''
#     - Yields nothing
#     - Renderable
#     - Contains expressions
#    '''
