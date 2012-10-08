
#class Module(object):

#class ModuleLevels(object):

#class Object(object):
#    '''
#     - Exists
#     - Has supers
#    '''

class Expression(object):
    '''
     - Yields a value of a certain type
     - Renderable
     - Is a complex ad-hoc structure of 
    '''
    
    enclosing = '%s' # No enclosing
    
    def __init__(self):
        raise NotImplementedError('lang.Expression.__init__ must not'
            ' be called directly')
    
    def yields(self, *types):
        try:
            self.get_a_yield_type(*types)
            return self
        except KeyError: #empty set
            raise Exception('Expected %s' % (', or '.join(types)))
    
    def get_yield_types(self):
        return self.yield_types
    
    def get_a_yield_type(self, *types):
        return set(types).intersection(set(self.get_yield_types())
            ).pop()
    
    def yield_(self, type_):
        return self
    
    def accept(self, expected):
        if not issubclass(self.__class__, expected):
            raise Exception('Expected %s, instead found %s'
                % (expected, self.__class__.__name__))
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
