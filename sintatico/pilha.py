from typing import List
from estado import Estado, SLR


class Pilha:
  __pilha: List

  def __init__(self, estadoInicial: Estado) -> None:
    self.__pilha = [estadoInicial]
  
  def inserir(self, estado: Estado):
    self.__pilha.append(estado)

  def remover(self) -> Estado:
    return self.__pilha.pop()

  def topo(self) -> Estado:
    return self.__pilha[-1]