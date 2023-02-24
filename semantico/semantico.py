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
    self.cont = 0
    self.identacao = 1
    pass

  def inserirPilha(self, lexema, tipo):
    tokenSemantico = {
      'simbolo': lexema,
      'terminal': True,
      'tipo': tipo
    }
    self.pilha.inserir(tokenSemantico)

  def executarRegra(self, numeroRegra, linha, coluna):
    self.linha = linha
    self.coluna = coluna
    func = getattr(Semantico, 'regra{}'.format(numeroRegra))
    func(self)
  

  def regra1(self):
    self.pilha.remover()
    tokenSemantico = {
      'simbolo' : "P'",
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)

  def regra2(self):
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'P',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)


  def regra3(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'v',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)


  def regra4(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'LV',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)    

  def regra5(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'LV',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)


  def regra6(self):
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()
    
    tokenSemantico = {
      'simbolo' : 'D',
      'terminal' : False,
      'lexema' : None
    }

    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo(';')


  def regra7(self):
    tokenSemanticoTipo = self.pilha.topo()
    
    lexema = self.pilha.topo(3)['simbolo']
    
    if tokenSemanticoTipo['tipo'] == 'REAL':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "REAL"
      self.tabelaSimbolos.atualizar(token)

    elif tokenSemanticoTipo['tipo'] == 'INTEIRO':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "INTEIRO"
      self.tabelaSimbolos.atualizar(token)
  
    elif tokenSemanticoTipo['tipo'] == 'LITERAL':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "LITERAL"
      self.tabelaSimbolos.atualizar(token)

    tokenSemantico = {
      'simbolo': 'L',
      'terminal': False,
      'tipo': tokenSemanticoTipo['tipo']
    }
    
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo(', {}'.format(lexema), False)


  def regra8(self):
    tokenSemanticoTipo = None

    for i in range(1, self.pilha.tamanho()):
      tokenSemanticoTipo = self.pilha.topo(i)

      if tokenSemanticoTipo['simbolo'] == 'TIPO' and tokenSemanticoTipo['terminal'] == False:
        break
    
    if tokenSemanticoTipo == None:
      raise Exception('Tipo não foi especificado')
    
    lexema = self.pilha.topo()['simbolo']
    
    if tokenSemanticoTipo['tipo'] == 'REAL':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "REAL"
      self.tabelaSimbolos.atualizar(token)

    elif tokenSemanticoTipo['tipo'] == 'INTEIRO':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "INTEIRO"
      self.tabelaSimbolos.atualizar(token)
  
    elif tokenSemanticoTipo['tipo'] == 'LITERAL':
      token = self.tabelaSimbolos.buscar(lexema)
      token['tipo'] = "LITERAL"
      self.tabelaSimbolos.atualizar(token)

    tokenSemantico = {
      'simbolo': 'L',
      'terminal': False,
      'tipo': tokenSemanticoTipo['tipo']
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo('{}'.format(lexema), False)


  def regra9(self):
    tokenSemantico = {
      'simbolo': 'TIPO',
      'terminal': False,
      'tipo': "INTEIRO"
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo('int', False)


  def regra10(self):
    tokenSemantico = {
      'simbolo': 'TIPO',
      'terminal': False,
      'tipo': "REAL"
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo('float', False)


  def regra11(self):
    tokenSemantico = {
      'simbolo': 'TIPO',
      'terminal': False,
      'tipo': "LITERAL"
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo('literal', False)


  def regra12(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'A',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)    


  def regra13(self):
    tokenSemanticoId = self.pilha.topo(2)

    token = self.tabelaSimbolos.buscar(tokenSemanticoId['simbolo'])

    if token['tipo'] == "LITERAL":
      self.escreveCodigo('scanf(\"%s\", {});'.format(token['lexema']))
    elif token['tipo'] == "INTEIRO":
      self.escreveCodigo('scanf(\"%d\", &{});'.format(token['lexema']))
    elif token['tipo'] == "REAL":
      self.escreveCodigo('scanf(\"%lf\", &{});'.format(token['lexema']))
    else:
      print("ERRO Semantico: Variável não declarada em linha {} coluna {}".format(self.linha-1, self.coluna))
      self.deveEscreverCodigo = False

    tokenSemantico = {
      'simbolo': 'ES',
      'terminal': False,
    }

    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)


  def regra14(self):
    tokenSemanticoARG = self.pilha.topo(2)
    tipo = tokenSemanticoARG['tipo'] if 'tipo' in tokenSemanticoARG else None

    if tipo == 'LITERAL':
      self.escreveCodigo('printf("%s", {});'.format(tokenSemanticoARG['lexema']))
    elif tipo == 'INTEIRO':
      self.escreveCodigo('printf("%d", {});'.format(tokenSemanticoARG['lexema']))
    elif tipo == 'REAL':
      self.escreveCodigo('printf("%f", {});'.format(tokenSemanticoARG['lexema']))
    else:
      self.escreveCodigo('printf("{}");'.format(tokenSemanticoARG['lexema']))

    tokenSemantico = {
      'simbolo' : 'ES',
      'terminal' : False,
    }

    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)
  
  
  def regra15(self):
    tokenSemanticoLit = self.pilha.topo()
    tokenSemantico = {
      'simbolo' : 'ARG',
      'terminal' : False,
      'lexema' : tokenSemanticoLit['simbolo'][1:-1]
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)

  def regra16(self):
    self.regra15()


  def regra17(self):
    tokenSemanticoId = self.pilha.topo()
    lexema = tokenSemanticoId['simbolo']
    token = self.tabelaSimbolos.buscar(lexema)

    tokenExiste = token != None and token['tipo'] != None

    if not tokenExiste:
      print("ERRO Semantico: Variável não declarada em linha {} coluna {}".format(self.linha-1, self.coluna))
      self.deveEscreverCodigo = False

    tokenSemantico = {
      'simbolo' : 'ARG',
      'terminal' : False,
      'tipo' : token["tipo"] if "tipo" in token else None,
      'lexema' : token["lexema"] if "lexema" in token else None
    }

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)


  def regra18(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'A',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)    


  def regra19(self):
    tokenSemanticoId = self.pilha.topo(4)
    tokenSemanticoRcb = self.pilha.topo(3)
    tokenSemanticoLD = self.pilha.topo(2)

    lexema = tokenSemanticoId['simbolo']
    token = self.tabelaSimbolos.buscar(lexema)

    # Busco pelo token pelo fato do id da pilha semantica ter perdido a referencia do id anteriormente declarado
    tokenEncontrado = token != None and token['tipo'] != None
    if tokenEncontrado:
      ehIgual = token['tipo'] == tokenSemanticoLD['tipo']
      if ehIgual:
        self.escreveCodigo('{} = {};'.format(tokenSemanticoId['simbolo'], tokenSemanticoLD['lexema']))
      else:
        print("ERRO Semantico: Tipos diferentes para atribuição em linha {} coluna {}".format(self.linha-1, self.coluna))
        self.deveEscreverCodigo = False
    else:
      print("ERRO Semantico: Variável não declarada em linha {} coluna {}".format(self.linha-1, self.coluna))
      self.deveEscreverCodigo = False

  def regra20(self):
    tokenSemanticoOPRD_1 = self.pilha.topo(3)
    tokenSemanticoOpa = self.pilha.topo(2)
    tokenSemanticoOPRD_2 = self.pilha.topo(1)

    tokenSemantico = {
      'simbolo' : 'LD',
      'terminal' : False,
      'lexema' : None,
      'tipo' : None,
    }

    self.cont += 1
    tokenSemantico['lexema'] = 'T{}'.format(self.cont)
    
    ###########################
    # VERIFICAR TIPO E LEXEMA #
    ###########################

    self.escreveCodigo('T{cont} = {oprd1_lexema} {opa_tipo} {oprd2_lexema};'.format(
                          cont=self.cont, oprd1_lexema=tokenSemanticoOPRD_1['lexema'],
                          opa_tipo=tokenSemanticoOpa['simbolo'],oprd2_lexema=tokenSemanticoOPRD_2['lexema']))
  
    ehDiferente = tokenSemanticoOPRD_1['tipo'] != tokenSemanticoOPRD_2['tipo']
    ehLiteral = tokenSemanticoOPRD_1['tipo'] == 'LITERAL' or tokenSemanticoOPRD_2['tipo'] == 'LITERAL'
    
    if ehLiteral:
      print('ERRO Semantico: Operandos com tipos incompatíveis em linha {} coluna {}'.format(self.linha-1, self.coluna))
      self.deveEscreverCodigo = False
   
    elif ehDiferente:
      tokenSemantico['tipo'] = 'REAL'
    else:
      tokenSemantico['tipo'] = 'INTEIRO'

    self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)


  def regra21(self):
    tokenSemanticoOPRD = self.pilha.topo()
    tokenSemantico = {}
    
    for key in tokenSemanticoOPRD:
      if key != 'simbolo':
        tokenSemantico[key] = tokenSemanticoOPRD[key]
    tokenSemantico['simbolo'] = 'LD'

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)


  def regra22(self):
    tokenSemanticoId = self.pilha.topo()
    lexema = tokenSemanticoId['simbolo']

    token = self.tabelaSimbolos.buscar(lexema)
    tokenSemantico = {
      'simbolo'  : 'OPRD',
      'terminal' : False,
      'lexema'   : None,
      'tipo'     : None
    }

    token_encontrado = token != None and token['tipo'] != None
    if token_encontrado:
      tokenSemantico['lexema'] = token['lexema']
      tokenSemantico['tipo'] = token['tipo']
    else:
      print('ERRO Semantico: Variável não declarada em linha {} coluna {}'.format(self.linha-1, self.coluna))
      self.deveEscreverCodigo = False

    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)


  def regra23(self):
    tokenSemanticoNum = self.pilha.topo()
    tokenSemantico = {
      'simbolo'  : 'OPRD',
      'terminal' : False,
      'lexema'   : tokenSemanticoNum['simbolo'],
      'tipo'     : tokenSemanticoNum['tipo']
    }
    
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)


  def regra24(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'A',
      'terminal': False,
    }

    self.pilha.inserir(tokenSemantico)
  

  def regra25(self):
    self.escreveCodigo('}')
    
    tokenSemantico = {
      'simbolo' : 'COND',
      'terminal': False,
      'lexema'  : None
    }

    self.pilha.remover()
    self.pilha.remover()
    self.pilha.inserir(tokenSemantico)
    

  def regra26(self):
    self.pilha.remover()
    self.pilha.remover()
    tokenSemanticoEXP_R = self.pilha.remover()
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'CAB',
      'terminal' : False,
    }
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo('if ({}) {{'.format(tokenSemanticoEXP_R['lexema']))
    self.identacao = self.identacao + 1

  def regra27(self):
    tokenSemanticoOPRD_2 = self.pilha.remover()
    tokenSemanticoOPR = self.pilha.remover()
    tokenSemanticoOPRD_1 = self.pilha.remover()

    oprd1EhNumero = tokenSemanticoOPRD_1['tipo'] in ('INTEIRO', 'REAL')
    oprd2EhNumero = tokenSemanticoOPRD_2['tipo'] in ('INTEIRO', 'REAL')
    ehDiferente = tokenSemanticoOPRD_1['tipo'] != tokenSemanticoOPRD_1['tipo']
    if (not oprd1EhNumero or not oprd2EhNumero):
      print("ERRO Semantico: Operandos com tipos incompatíveis em linha {} coluna {}".format(self.linha-1, self.coluna))
      self.deveEscreverCodigo = False
  
    self.cont = self.cont + 1
    variavelTemporaria = 'T{}'.format(self.cont)

    tokenSemantico = {
      'simbolo' : 'EXP_R',
      'terminal' : False,
      'lexema' :  variavelTemporaria
    }
    self.pilha.inserir(tokenSemantico)

    self.escreveCodigo('{} = {} {} {};'.format(variavelTemporaria, tokenSemanticoOPRD_1['lexema'], tokenSemanticoOPR['simbolo'], tokenSemanticoOPRD_2['lexema']))

  def regra28(self):
    self.pilha.remover()
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'CP',
      'terminal' : False
    }

    self.pilha.inserir(tokenSemantico)    

  def regra29(self):
    self.regra28()

  def regra30(self):
    self.regra28()

  def regra31(self):
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'CP',
      'terminal' : False,
    }
    self.pilha.inserir(tokenSemantico)

    self.identacao = self.identacao - 1
    #self.escreveCodigo('}')

  def regra32(self):
    self.pilha.remover()

    tokenSemantico = {
      'simbolo' : 'A',
      'terminal' : False,
    }
    self.pilha.inserir(tokenSemantico)

    self.identacao = self.identacao - 1
    self.escreveCodigo('}')
    self.escreveCabecalho()

  def escreveCodigo(self, texto, novaLinha = True):
    if self.deveEscreverCodigo == False:
      return

    for i in range (0, self.identacao):
      self.codigoGerado = self.codigoGerado + "\t"

    self.codigoGerado = self.codigoGerado + texto + ("\n" if novaLinha else "")


  def imprimeCodigo(self):
    if self.deveEscreverCodigo == False:
      return
    
    caminho_arquivo: str = '{path}/../output.c'.format(path=dirname(realpath(__file__)))
    arquivo = open(caminho_arquivo, 'w')
    arquivo.write(self.codigoGerado)

  def escreveCabecalho(self):
    if self.deveEscreverCodigo == False:
      return

    cabecalho = ''
    cabecalho = cabecalho + '#include <stdio.h>\n'
    cabecalho = cabecalho + 'typedef char literal[256];\n'
    cabecalho = cabecalho + 'void main(void)\n'
    cabecalho = cabecalho + '{\n'
    cabecalho = cabecalho + '\t/*----Variaveis temporarias----*/\n'

    for i in range (0, self.cont):
      cabecalho = cabecalho + '\tint T{};\n'.format(i + 1)

    cabecalho = cabecalho + '\t/*------------------------------*/\n'

    self.codigoGerado = cabecalho + self.codigoGerado