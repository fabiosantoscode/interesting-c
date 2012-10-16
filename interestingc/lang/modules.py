

class Module(list):
    def __init__(self, *args):
        return super(Module, self).__init__(args)
    def accept(self, *args, **kwargs):
        if not len(self) == 1:
            raise Exception
        return self[0].accept(*args, **kwargs)
