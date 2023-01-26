import sys
from os.path import realpath, dirname

path = '{path}/../lexico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

from tokenLexico import Token
from scanner import SCANNER
from pilha import Pilha
from mapaTransicoes import MapaTransicoes, Acoes
from error_recovery import Recovery

def analisador():
  pilha = Pilha(0)
  mapaTransicoes = MapaTransicoes()
  caminho_arquivo: str = '{path}/teste.txt'.format(path=dirname(realpath(__file__)))
  arquivo = open(caminho_arquivo, 'r')

  token: Token = SCANNER(arquivo)
  while 1:
    estadoAtual = pilha.topo()
    entrada = token['classe']
    estado = mapaTransicoes.shiftReduceError[estadoAtual][entrada]

    if estado["acao"].value == Acoes.SHIFT.value:
      pilha.inserir(estado["estado"])
      token = SCANNER(arquivo)
    elif estado["acao"].value == Acoes.REDUCE.value:
      for estadoEmpilhado in estado["direita"]:
        pilha.remover()

      pilha.inserir(mapaTransicoes.goto[pilha.topo()][estado["esquerda"]])
      print("Redução: {esquerda} -> {direita}".format(esquerda=estado["esquerda"], direita=estado["direita"]))

    elif estado["acao"].value == Acoes.ACCEPT.value:
        pilha.remover()
        print("Redução: {esquerda} -> {direita}".format(esquerda=estado["esquerda"], direita=estado["direita"]))
        break
    else:
      print('TOKEN: {}'.format(token))
      #rotina de erro
      print('Rotina de erro invocada')
      pilha, token = Recovery(pilha, token, SCANNER, arquivo, mapaTransicoes).panic_mode(token)
      if pilha == None:
        print('Recuperacao falhou...')
        break
      else:
        print('rotina funcionou')
      pass
  arquivo.close()

analisador()