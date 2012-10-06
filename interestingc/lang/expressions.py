import lang

class DecimalNumberLiteral(lang.Expression):
    yield_type = 'int'
    
    def __init__(self, value):
        self.value = value
    
    def render(self):
        return str(self.value)
    
