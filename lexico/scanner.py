from enum import Enum
from typing import Any
import afd
from tokenLexico import Token, Classes
from tabelaSimbolos import tabelaSimbolos
import sys
from errosLexicos import ErrosLexicos



class Scan:
  num_linha: int
  num_coluna: int
  arquivo: Any
  caractere: str
  afd: afd.AFD

  def __init__(self) -> None:
    self.num_linha = 1
    self.num_coluna = 0
    self.arquivo = None
    self.caractere = ' '
    self.afd = afd.AFD()

  def ler_proximo_caractere(self):
    if self.caractere in ['\n', '\r']:
      self.num_linha = self.num_linha + 1
      self.num_coluna = 0

    self.caractere = self.arquivo.read(1)

    self.num_coluna = self.num_coluna + 1

  def scanner(self, arquivo):
    if self.arquivo == None:
      self.arquivo = arquivo

    while 1:
      afd_parou, lexema, erro = self.afd.transicao(self.caractere)

      if not afd_parou:
        self.ler_proximo_caractere()
        continue

      token: Token = { 
        "classe": self.afd.estado_atual.token_class.value,
        "lexema": lexema,
        "tipo": self.afd.estado_atual.token_type.value,
      }
      self.afd.volta_inicio()

      if token["classe"] == Classes.COMENTARIO.value:
        self.ler_proximo_caractere()
        continue

      elif token["classe"] == Classes.ERRO.value:
        if erro == ErrosLexicos.CARACTERE_INVALIDO.value:
          mensagem_erro = "ERRO LÉXICO - Caractere inválido, linha {num_linha}, coluna {num_coluna}".format(num_linha = self.num_linha, num_coluna = self.num_coluna)
          self.ler_proximo_caractere()
        elif erro == ErrosLexicos.LEXEMA_MAL_FORMADO.value:
          mensagem_erro = "ERRO LÉXICO - Lexema mal formado, linha {num_linha}, coluna {num_coluna}".format(num_linha = self.num_linha, num_coluna = self.num_coluna - 1)
        elif erro == ErrosLexicos.LITERAL_INCOMPLETA.value:
          mensagem_erro = "ERRO LÉXICO - Literal não fechada, linha {num_linha}, coluna {num_coluna}".format(num_linha = self.num_linha, num_coluna = self.num_coluna - 1)
        elif erro == ErrosLexicos.COMENTARIO_INCOMPLETO.value:
          mensagem_erro = "ERRO LÉXICO - Comentário não fechado, linha {num_linha}, coluna {num_coluna}".format(num_linha = self.num_linha, num_coluna = self.num_coluna - 1)
        print(mensagem_erro)

      elif token["classe"] == Classes.ID.value:
        token_existente = tabelaSimbolos.buscar(lexema)
        if token_existente == None:
          tabelaSimbolos.inserir(token)
        else:
          token = token_existente

      return token, (self.num_linha, self.num_coluna)

scan = Scan()
def SCANNER(arquivo) -> Token:
  return scan.scanner(arquivo)

