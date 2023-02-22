import sys
from os.path import realpath, dirname

path = '{path}/../lexico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

path = '{path}/../semantico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

import copy
from tokenLexico import Token
from scanner import SCANNER
from pilha import Pilha
from mapaTransicoes import MapaTransicoes, Acoes
from error_recovery import Recovery
from semantico import Semantico
from tabelaSimbolos import tabelaSimbolos

def analisador():
  pilha = Pilha(0)
  mapaTransicoes = MapaTransicoes()
  semantico = Semantico(tabelaSimbolos)
  caminho_arquivo: str = '{path}/teste.txt'.format(path=dirname(realpath(__file__)))
  arquivo = open(caminho_arquivo, 'r')

  token: Token
  posicao: tuple
  posicao_ultimo_erro : int
  token, posicao = SCANNER(arquivo)
  posicao_ultimo_erro = '*'
  map_tokens = {
      'LIT' : '"', 
      'COMENTARIO':  ["{","}"],
      'OPR' : [">", "<",  "="], 
      'OPA' :  ["/","*","-","+"], 
      'VIR' : ",",
      'PT_V' : ";",
      'AB_P' : "(",
      'FC_P' : ")",
      'ATR' : "<-"
}
  while 1:
    estadoAtual = pilha.topo()
    entrada = token['classe']
    if entrada != "ERRO":
      estado = mapaTransicoes.shiftReduceError[estadoAtual][entrada]

      if estado["acao"].value == Acoes.SHIFT.value:
        pilha.inserir(estado["estado"])

        semantico.inserirPilha(token["lexema"], token["tipo"])

        token, posicao = SCANNER(arquivo)

      elif estado["acao"].value == Acoes.REDUCE.value:
        for estadoEmpilhado in estado["direita"]:
          pilha.remover()
      
        try:
          pilha.inserir(mapaTransicoes.goto[pilha.topo()][estado["esquerda"]])
        except:
          print('ERRO GOTO')
          print('{} Para a entrada {}'.format(pilha.topo(), estado['esquerda']))
          
        print("Redução regra {regra}: {esquerda} -> {direita}".format(regra=estado["regra"], esquerda=estado["esquerda"], direita=estado["direita"]))

        semantico.executarRegra(estado["regra"], posicao[0], posicao[1])

      elif estado["acao"].value == Acoes.ACCEPT.value:
          pilha.remover()
          print("Aceita regra 1: {esquerda} -> {direita}".format(esquerda=estado["esquerda"], direita=estado["direita"]))
          semantico.imprimeCodigo()
          break
      else:
        #rotina de erro
        semantico.deveEscreverCodigo = False
        estado_erro = mapaTransicoes.shiftReduceError[pilha.topo()]
        tokens_esperados_temp = [x for x in estado_erro if estado_erro[x]['acao'].value != Acoes.ERROR.value] 
        tokens_esperados = []
        for x in tokens_esperados_temp:
          if x in map_tokens:
            tokens_esperados.append(map_tokens[x])
          else:
            tokens_esperados.append(x)
        del tokens_esperados_temp
        if posicao_ultimo_erro != posicao:
          print('Erro na linha {} coluna {}, ao identificar o token "{}", eram esperados um dos tokens"{}"'.format(posicao[0],posicao[1],token['lexema'], tokens_esperados))

        token, pilha = Recovery(pilha, token, SCANNER, arquivo, mapaTransicoes, posicao, posicao_ultimo_erro, caminho_arquivo, map_tokens).recovery_token
        posicao_ultimo_erro = posicao
       
        if token == None or token == 0:
          print('Recuperacao falhou...')
          break
        else:
          pass
    else:
      semantico.deveEscreverCodigo = False
      token, posicao = SCANNER(arquivo)
  arquivo.close()

analisador()