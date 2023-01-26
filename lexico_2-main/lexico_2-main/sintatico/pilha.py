from typing import List

class Pilha:
  __pilha: List

  def __init__(self, estadoInicial: int) -> None:
    self.__pilha = [estadoInicial]
  
  def inserir(self, estado: int):
    self.__pilha.append(estado)

  def remover(self) -> int:
    return self.__pilha.pop()

  def topo(self) -> int:
    return self.__pilha[-1]

  
  def len(self) -> int:
    return len(self.__pilha)