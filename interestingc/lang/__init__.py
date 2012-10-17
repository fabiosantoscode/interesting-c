
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
     - Yields a value of a certain type
     - Renderable
     - Can be a complex ad-hoc modifiable syntax tree.
    '''
    
    def get_yield_type(self):
        return self.yield_type
    
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
