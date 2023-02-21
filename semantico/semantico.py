from os.path import realpath, dirname
from pilhaSemantica import Pilha

class Semantico:
  def __init__(self, tabelaSimbolos) -> None:
    self.pilha = Pilha()
    self.tabelaSimbolos = tabelaSimbolos
    self.codigoGerado = ''
    self.deveEscreverCodigo = True
    self.linha = 0
    self.coluna = 0
    pass

  def inserirPilha(self, lexema):
    tokenSemantico = {
      'simbolo': lexema,
      'terminal': True
    }
    self.pilha.inserir(tokenSemantico)

  def executarRegra(self, numeroRegra, linha, coluna):
    self.linha = linha
    self.coluna = coluna
    func = getattr(Semantico, 'regra{}'.format(numeroRegra))
    func(self)

  def regra7(self):
    tokenSemanticoTipo = self.pilha.topo()
    
    lexema = self.pilha.topo(2)['simbolo']
    
    if tokenSemanticoTipo['tipo'] == 'real':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "REAL"
      self.tabelaSimbolos.atualizar(token)

          
    if tokenSemanticoTipo['tipo'] == 'inteiro':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "INTEIRO"
      self.tabelaSimbolos.atualizar(token)

    tokenSemantico = {
      'simbolo': 'L',
      'terminal': False,
      'tipo': tokenSemanticoTipo['tipo']
    }
    
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def regra8(self):
    tokenSemanticoTipo = None

    for i in range(1, self.pilha.tamanho()):
      tokenSemanticoTipo = self.pilha.topo(i)

      if tokenSemanticoTipo['simbolo'] == 'TIPO' and tokenSemanticoTipo['terminal'] == False:
        break
    
    if tokenSemanticoTipo == None:
      raise Exception('Tipo não foi especificado')
    
    lexema = self.pilha.topo()['simbolo']
    
    if tokenSemanticoTipo['tipo'] == 'real':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "REAL"
      self.tabelaSimbolos.atualizar(token)

          
    if tokenSemanticoTipo['tipo'] == 'inteiro':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "INTEIRO"
      self.tabelaSimbolos.atualizar(token)

    tokenSemantico = {
      'simbolo': 'L',
      'terminal': False,
      'tipo': tokenSemanticoTipo['tipo']
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def regra9(self):
    tokenSemantico = {
      'simbolo': 'TIPO',
      'terminal': False,
      'tipo': "INTEIRO"
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def regra10(self):
    tokenSemantico = {
      'simbolo': 'TIPO',
      'terminal': False,
      'tipo': "REAL"
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def regra11(self):
    tokenSemantico = {
      'simbolo': 'TIPO',
      'terminal': False,
      'tipo': "LITERAL"
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def regra13(self):
    tokenSemanticoId = self.pilha.topo(2)

    if tokenSemanticoId['tipo'] == "LITERAL":
      self.escreveCodigo('scanf(\"%s\", id.lexema);')
    elif tokenSemanticoId['tipo'] == "INTEIRO":
      self.escreveCodigo('scanf(\"%d\", &id.lexema);')
    elif tokenSemanticoId['tipo'] == "REAL":
      self.escreveCodigo('scanf(\"%lf\", &id.lexema);')
    else:
      print("Variável não declarada em linha {linha} coluna {coluna}".format(linha=self.linha, coluna=self.coluna))

    tokenSemantico = {
      'simbolo': 'ES',
      'terminal': False,
    }

    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def escreveCodigo(self, texto):
    if self.deveEscreverCodigo == True:
      self.codigoGerado = self.codigoGerado + texto + "\n"

  def imprimeCodigo(self):
    if self.deveEscreverCodigo == False:
      return
    
    caminho_arquivo: str = '{path}/../output.c'.format(path=dirname(realpath(__file__)))
    arquivo = open(caminho_arquivo, 'w')
    arquivo.write(self.codigoGerado)