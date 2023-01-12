import sys
from os.path import realpath, dirname

path = '{path}/../lexico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

from tokenLexico import Classes, Token
from scanner import SCANNER
from pilha import Pilha
from estado import SLR
from mapaTransicoes import shiftReduceError, goto, Acoes


def analisador():
  slr = SLR()
  pilha = Pilha(slr._estados[0])
  caminho_arquivo: str = '{path}/teste.txt'.format(path=dirname(realpath(__file__)))
  arquivo = open(caminho_arquivo, 'r')

  token: Token = SCANNER(arquivo)
  print("Token reconhecido", token)
  while 1:
    estadoAtual = pilha.topo()
    entrada = token['classe']
    estado = shiftReduceError[estadoAtual.id][entrada.value]

    if estado["acao"].value == Acoes.SHIFT.value:
      pilha.inserir(slr._estados[estado["estado"]])
      token = SCANNER(arquivo)
      print("Token reconhecido", token)
    elif estado["acao"].value == Acoes.REDUCE.value:
      for estadoEmpilhado in estado["direita"].reverse():
        if pilha.remover() != estadoEmpilhado:
          raise Exception("Erro na redução: simbolo não esperado")

        pilha.inserir(goto[pilha.topo.id][estado["esquerda"]])
        print("Redução: {esquerda} -> {direita}".format(esquerda=estado["esquerda"], direita=estado["direita"]))
    elif estado["acao"].value == Acoes.REDUCE.value:
      break
    else:
      #rotina de erro
      pass

  print("saiu", token['classe']), 
  arquivo.close()

analisador()