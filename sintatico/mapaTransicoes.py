from enum import Enum
from naoTerminais import NaoTerminais
from tokenLexico import Classes
from palavrasReservadas import PalavrasReservadas

class Acoes(Enum):
  SHIFT = "shift"
  REDUCE = "reduce"
  ACCEPT = "accept"
  ERROR = "error"

shiftReduceError = [
  #Estado 0
  {
    "inicio": {
      "acao": Acoes.SHIFT,
      "estado": 2
    },
  },
  #Estado 3
  {
    "fim": {
      "fim": Acoes.REDUCE,
      "esquerda": "A",
      "direita": ["fim"],
    }
  }
]

goto = [
  #Estado 0
  {"P": 1} 
]