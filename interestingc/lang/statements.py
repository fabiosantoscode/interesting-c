import unittest
import lang
import expressions
from collections import namedtuple



class Statement(object):
    '''
     - Yields nothing
     - Renderable
     - Contains expressions
    '''
    
    def to_c(self):
        raise NotImplementedError
    
    def __init__():
        raise NotImplementedError('lang.Statement must not be '
            'initialized directly')



class Assignment(Statement):
    def __init__(self, assignee, expression):
        self.expression = expression.accept(lang.Expression)
        self.assignee = assignee.accept(lang.Identifier)



class ContainerStatement(Statement):
    '''Abstracts an expression from other kinds of statements.'''
    def __init__(self, containee):
        self.containee = containee
    
    def get_own_type(self):
        return self.containee.__class__
    
    def to_c(self):
        return self.containee.to_c()

