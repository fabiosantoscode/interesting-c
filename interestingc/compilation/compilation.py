'''
interesting-c compiler. Gets code through several stages until compilation
'''

import os.path
import os
from parse.parse import parse_module


class Compiler(object):
    '''Compiles an interesting-c program'''
    
    def compile_(self, filename):
        with open(filename) as fp:
            self.compile_file(fp)
    
    def compile_file(self, fp):
        self.root = parse_module(fp.read())
    
    def write_file(self, out_file):
        assert hasattr(self, 'root')
        self.root.file_write(out_file)

