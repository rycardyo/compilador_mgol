from typing import List

class Pilha:
  __pilha: List

  def __init__(self, estadoInicial: int) -> None:
    self.__pilha = [estadoInicial]
  
  def inserir(self, estado: int):
    self.__pilha.append(estado)

  def remover(self) -> int:
    return self.__pilha.pop()

  def topo(self, offset = 1) -> int:
    return self.__pilha[-offset]

  def tamanho(self) -> int:
    return self.__pilha.count()
  
  def len(self) -> int:
    return len(self.__pilha)