from typing import List

class Pilha:
  __pilha: List

  def __init__(self) -> None:
    self.__pilha = []
  
  def inserir(self, tokenSemantico):
    self.__pilha.append(tokenSemantico)

  def remover(self) -> int:
    return self.__pilha.pop()

  def topo(self, offset = 1) -> int:
    return self.__pilha[-offset]

  def tamanho(self) -> int:
    return len(self.__pilha)
  
  def len(self) -> int:
    return len(self.__pilha)