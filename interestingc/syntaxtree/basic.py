
from tree import SyntaxTreeNode

#class Module(object):

#class ModuleLevels(object):

#class Object(object):
#    '''
#     - Exists
#     - Has supers (or not)
#     - Has attributes, as struct members
#    '''

class Expression(SyntaxTreeNode):
    '''
        Yields a value of a certain type
        There is a type of expression, which is its __class__.
    get_own_type gets __class__, but it can be overridden to fake
    other types and make some expressions transparent.
        Renderable
        May have side effects
    '''
    
    def get_yield_type(self):
        return self.yield_type
    
    def get_own_type(self):
        return self.__class__
    
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



class Statement(object):
    '''
     - Yields nothing, but almost always has side effects.
     - Renderable
     - Contains expressions
    '''
    
    

