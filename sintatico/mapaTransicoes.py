from enum import Enum
import csv
from os.path import realpath, dirname

class Acoes(Enum):
  SHIFT = "shift"
  REDUCE = "reduce"
  ACCEPT = "accept"
  ERROR = "error"

class MapaTransicoes:
  def __init__(self) -> None:
    self.shiftReduceError = {}
    self.goto = {}

    caminhoShiftReduce: str = '{path}/Shift-Reduce.csv'.format(path=dirname(realpath(__file__)))
    with open(caminhoShiftReduce, 'r') as shiftReduceCSV:
      reader = csv.DictReader(shiftReduceCSV)
      for estado, simbolos in enumerate(reader):
          self.shiftReduceError[estado] = {}

          for simbolo in simbolos:
            comandoSerializado = simbolos[simbolo]
            if (comandoSerializado == ''):
              continue

            comando = comandoSerializado.split('-')
            acao = comando[0]

            if acao == 'S':
              estadoShift = comando[1]
              self.shiftReduceError[estado][simbolo] = {
                "acao": Acoes.SHIFT,
                "estado": int(estadoShift),
              }
            elif acao == 'R':
              regra = int(comando[1])
              ladoEsquerdo = comando[2]
              ladoDireito = comando[3].split(' ')
              self.shiftReduceError[estado][simbolo] = {
                "acao": Acoes.REDUCE,
                "regra": regra,
                "esquerda": ladoEsquerdo,
                "direita": ladoDireito,
              }
            elif acao == 'A':
              ladoEsquerdo = comando[1]
              ladoDireito = comando[2].split(' ')
              self.shiftReduceError[estado][simbolo] = {
                "acao": Acoes.ACCEPT,
                "esquerda": ladoEsquerdo,
                "direita": ladoDireito,
              }
            elif acao == 'E':
              codigo = comando[1]
              self.shiftReduceError[estado][simbolo] = {
                "acao": Acoes.ERROR,
                "codigo": int(codigo)
              }
            else:
              raise Exception("Erro desconhecido")
    
    caminhoGoto: str = '{path}/Goto.csv'.format(path=dirname(realpath(__file__)))
    with open(caminhoGoto, 'r') as gotoCSV:
      reader = csv.DictReader(gotoCSV)
      for estado, simbolos in enumerate(reader):
          self.goto[estado] = {}

          for simbolo in simbolos:
            comandoSerializado = simbolos[simbolo]
            if (comandoSerializado == ''):
              continue

            comando = comandoSerializado.split('-')
            acao = comando[0]

            if acao == 'G':
              estadoGoto = comando[1]
              self.goto[estado][simbolo] = int(estadoGoto)
            else:
              raise Exception("Erro desconhecido")