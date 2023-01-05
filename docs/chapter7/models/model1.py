a = 1
b = 2

def test(a,b):
    return a+b

class User(object):
    def __init__(self,a,b):
        self.a = a
        self.b = b
        
    def sums(self):
        return self.a + self.b
    
    def muls(self):
        return self.a * self.b
    

def __group():
    return 1