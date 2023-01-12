from typing import List, Dict, Union
from tokenLexico import Classes
from naoTerminais import NaoTerminais


class Estado():
    id: int
    acoes: Dict[Union[Classes, NaoTerminais], dict]

    def __init__(self, id: int, transicoes: dict) -> None:
        self.id = id
        self.transicoes = transicoes

class SLR:
    _estados: dict

    def __init__(self, mapaTransicoes: List) -> None:
        self._estados = {}

        for indice, transicoes in enumerate(mapaTransicoes):
            estado = Estado(indice, transicoes)
            self._estados[indice] = estado