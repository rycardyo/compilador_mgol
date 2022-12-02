from enum import Enum
from typing import Dict, Optional

from tokenLexico import Token

class PalavrasReservadas(Enum):
  INICIO = "inicio"
  VARINICIO = "varinicio"
  VARFIM = "varfim"
  ESCREVA = "escreva"
  LEIA = "leia"
  SE = "se"
  ENTAO = "entao"
  FIMSE = "fimse"
  FIM = "fim"
  INTEIRO = "inteiro"
  LITERAL = "literal"
  REAL = "real"


class TabelaSimbolos:
  __simbolos: Dict[str, Token]

  def __init__(self) -> None:
    self.__simbolos = {}

    for palavraReservada in PalavrasReservadas:
      token: Token = { 
        "classe": palavraReservada.value,
        "lexema": palavraReservada.value,
        "tipo":palavraReservada.value,
      }
      self.__simbolos[token["lexema"]] = token
  
  def inserir(self, token: Token) -> Token:
    if token["lexema"] in self.__simbolos:
      raise Exception("Token já existe")

    self.__simbolos[token["lexema"]] = token

    return token

  def buscar(self, lexema: str) -> Optional[Token]:
    if lexema in self.__simbolos:
      return self.__simbolos[lexema]

    return None

  def atualizar(self, token: Token) -> Token:
    if token["lexema"] not in self.__simbolos:
      raise Exception("Token não existe")

    self.__simbolos[token["lexema"]] = token

    return token

tabelaSimbolos = TabelaSimbolos()