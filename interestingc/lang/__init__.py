
#class Module(object):

#class ModuleLevels(object):

#class Object(object):
#    '''
#     - Exists
#     - Has supers
#    '''

class Expression(object):
    '''
     - Yields something of a certain type
     - Renderable
     - Can contain itself
    '''
    
    def __init__(self, containee):
        self.containee = containee.accept(Expression)
    
    def get_type(self):
        return self.yield_type
    
    def yield_(self):
        raise NotImplementedError('Expression yield_ needs to yield something ')
    
    def accept(self, expected):
        if not issubclass(self.__class__, expected):
            raise Exception('Expected %s, instead found %s' % (expected, self.__class__.__name__))
        else:
            return self
    
    def render(self):
        raise NotImplementedError
    

#class Statement(object):
#    '''
#     - Yields nothing
#     - Renderable
#     - Contains expressions
#    '''
