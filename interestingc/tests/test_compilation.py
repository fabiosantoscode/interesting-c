import unittest
from StringIO import StringIO

from compilation.compilation import Compiler



class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.cfile = StringIO('''
            int main(int argc, char* argv[]){
                return 0;
            }''')
    
    def test_compiler(self):
        compiler = Compiler()
        compiler.compile_file(self.cfile)
