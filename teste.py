import sys 
sys.path.insert(0,'./lexico')

class Oi:
    def __init__(self):
        acoes = [self.f1,self.f2,self.f3]
        
        for acao in acoes:
            acao()
    
    def f1(self):
        print('fs1')

    def f2(self):
        print('f2')

    def f3(self):
        print('f3')

Oi()