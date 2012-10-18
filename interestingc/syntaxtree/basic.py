
from tree import SyntaxTreeNode

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

