from typing import Dict, List, Tuple
from enum import Enum
from errosLexicos import ErrosLexicos
import tokenLexico as token

class ClassesEntrada(Enum):
  LETRA = 'L'
  DIGITO = 'D'
  CORINGA = 'C'
  IGNORAR = 'I'
  EOF = '$'

class Estado():
    id: int
    final: bool = False
    token_class: token.Classes = token.Classes.NONE
    token_type: token.Tipos = token.Tipos.NONE
    transicoes: dict = {}

    def __init__(self, id: int) -> None:
        self.id = id
        self.final = False
        self.token_class = token.Classes.NONE
        self.token_type = token.Tipos.NONE
        self.transicoes = {}

    def gera_transicoes(self, entradas: List[str], estado_destino):
        for entrada in entradas:
            self.transicoes[entrada] = estado_destino

    def define_estado_final(self, token_class: token.Classes, token_type: token.Tipos = token.Tipos.NONE) -> None:
        self.final = True 
        self.token_class = token_class
        self.token_type = token_type

class AFD():
    _estados : List[Estado]
    _tabela_transicoes: Dict[str, dict]
    estado_atual: Estado
    caminho_percorrido: str

    def inicia_estados(self) -> None:
        self._estados = [Estado(id = i) for i in range(28)]

        # Estado 0
        self._estados[0].gera_transicoes([ClassesEntrada.IGNORAR.value], self._estados[0])
        self._estados[0].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[1])
        self._estados[0].gera_transicoes([ClassesEntrada.LETRA.value], self._estados[7])
        self._estados[0].gera_transicoes(['"'], self._estados[8])
        self._estados[0].gera_transicoes(["{"], self._estados[11])
        self._estados[0].gera_transicoes([ClassesEntrada.EOF.value], self._estados[14])
        self._estados[0].gera_transicoes([">"], self._estados[15])
        self._estados[0].gera_transicoes(["<"], self._estados[17])
        self._estados[0].gera_transicoes(["="], self._estados[21])
        self._estados[0].gera_transicoes(["/","*","-","+"], self._estados[22])
        self._estados[0].gera_transicoes([","], self._estados[23])
        self._estados[0].gera_transicoes([";"], self._estados[24])
        self._estados[0].gera_transicoes(["("], self._estados[25])
        self._estados[0].gera_transicoes([")"], self._estados[26])
        
        # Estado 01
        self._estados[1].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[1])
        self._estados[1].gera_transicoes(["."], self._estados[2])
        self._estados[1].gera_transicoes(["e","E"], self._estados[4])
        self._estados[1].define_estado_final(token.Classes.NUM, token.Tipos.INTEIRO)

        # Estado 02
        self._estados[2].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[3])

        # Estado 03
        self._estados[3].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[3])
        self._estados[3].gera_transicoes(["e","E"], self._estados[4])
        self._estados[3].define_estado_final(token.Classes.NUM, token.Tipos.REAL)
        
        # Estado 04
        self._estados[4].gera_transicoes(['+','-'], self._estados[5])
        self._estados[4].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[6])

        # Estado 05
        self._estados[5] = self._estados[5]
        self._estados[5].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[6])

        # Estado 06
        self._estados[6].gera_transicoes([ClassesEntrada.DIGITO.value], self._estados[6])
        self._estados[6].define_estado_final(token.Classes.NUM, token.Tipos.REAL)

        # Estado 07
        self._estados[7].gera_transicoes([ClassesEntrada.DIGITO.value] + [ClassesEntrada.LETRA.value] + ['_'], self._estados[7])
        self._estados[7].define_estado_final(token.Classes.ID)

        # Estado 08
        self._estados[8].gera_transicoes([ClassesEntrada.CORINGA.value], self._estados[9])
        self._estados[8].gera_transicoes(['"'], self._estados[10])

        # Estado 09
        self._estados[9].gera_transicoes([ClassesEntrada.CORINGA.value], self._estados[9])
        self._estados[9].gera_transicoes(['"'], self._estados[10])

        # Estado 10
        # Estado final sem transições
        self._estados[10].define_estado_final(token.Classes.LIT, token.Tipos.LITERAL)
        
        # Estado 11
        self._estados[11].gera_transicoes([ClassesEntrada.CORINGA.value], self._estados[12])
        self._estados[11].gera_transicoes(['}'], self._estados[13])

        # Estado 12
        self._estados[12].gera_transicoes([ClassesEntrada.CORINGA.value], self._estados[12])
        self._estados[12].gera_transicoes(['}'], self._estados[13])

        # Estado 13
        # Estado final sem transições
        self._estados[13].define_estado_final(token.Classes.COMENTARIO)

        # Estado 14
        # Estado final sem transições
        self._estados[14].define_estado_final(token.Classes.EOF)

        # Estado 15
        self._estados[15].gera_transicoes(['='], self._estados[16])
        self._estados[15].define_estado_final(token.Classes.OPR)

        # Estado 16
        # Estado final sem transições
        self._estados[16].define_estado_final(token.Classes.OPR)

        # Estado 17
        self._estados[17].gera_transicoes(['='], self._estados[18])
        self._estados[17].gera_transicoes(['<'], self._estados[19])
        self._estados[17].gera_transicoes(['-'], self._estados[20])
        self._estados[17].define_estado_final(token.Classes.OPR)

        # Estado 18
        # Estado final sem transicoes
        self._estados[18].define_estado_final(token.Classes.OPR)

        # Estado 19
        # Estado final sem transicoes
        self._estados[19].define_estado_final(token.Classes.OPR)

        # Estado 20
        # Estado final sem transicoes
        self._estados[20].define_estado_final(token.Classes.ATR)

        # Estado 21
        # Estado final sem transicoes
        self._estados[21].define_estado_final(token.Classes.OPR)
        
        # Estado 22
        # Estado final sem transicoes
        self._estados[22].define_estado_final(token.Classes.OPA)

        # Estado 23
        # Estado final sem transicoes
        self._estados[23].define_estado_final(token.Classes.VIR)

        # Estado 24
        # Estado final sem transicoes
        self._estados[24].define_estado_final(token.Classes.PT_V)

        # Estado 25
        # Estado final sem transicoes
        self._estados[25].define_estado_final(token.Classes.AB_P)

        # Estado 26
        # Estado final sem transicoes
        self._estados[26].define_estado_final(token.Classes.FC_P)

        # Estado 27
        # Estado final sem transicoes
        self._estados[27].define_estado_final(token.Classes.ERRO)
        
    def __init__(self) -> None:
        self.ALFABETO_LETRAS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.ALFABETO_LETRAS = self.ALFABETO_LETRAS + [x.upper() for x in self.ALFABETO_LETRAS]
        self.ALFABETO_DIGITOS = [str(x) for x in range(10)]
        self.ALFABETO_DEMAIS_CARACTERS = [',', ';', ':', '.', '!', '?', '*', '+', '-', '/', '(', ')', '[',']', '<', '>', '=', '\'', '\"', '{', '}', '_']
        self.ALFABETO_IGNORAR = [' ', '\n', '\r', '\t']
        self.ALFABETO_EOF = ['']
        self.ALFABETO = self.ALFABETO_DIGITOS + self.ALFABETO_LETRAS + self.ALFABETO_DEMAIS_CARACTERS + self.ALFABETO_IGNORAR + self.ALFABETO_EOF

        self.inicia_estados()

        self.volta_inicio()

    def transicao(self, caractere : str) -> Tuple[bool, str, int]:
        entrada = self.caractere_para_entrada(caractere)
        eh_comentario = self.estado_atual in [self._estados[11], self._estados[12]]
        eh_literal = self.estado_atual in [self._estados[8], self._estados[9]]

        if eh_literal:
            if entrada == token.Classes.EOF.value:
                self.estado_atual = self._estados[27]
                return True, self.caminho_percorrido, ErrosLexicos.LITERAL_INCOMPLETA.value
            elif entrada != "\"":
                entrada = ClassesEntrada.CORINGA.value


        if eh_comentario:
            if entrada == token.Classes.EOF.value:
                self.estado_atual = self._estados[27]
                return True, self.caminho_percorrido, ErrosLexicos.COMENTARIO_INCOMPLETO.value
            elif entrada != "}":
                entrada = ClassesEntrada.CORINGA.value
        
        existe_transicao = entrada in self.estado_atual.transicoes
        if existe_transicao:
            self.estado_atual = self.estado_atual.transicoes[entrada]

            if entrada != ClassesEntrada.IGNORAR.value:
                self.caminho_percorrido = self.caminho_percorrido + caractere

            terminou = entrada == ClassesEntrada.EOF.value
            return terminou, self.caminho_percorrido, None

        if not self.estado_atual.final:
            erro_estado_inicial = self.estado_atual == self._estados[0]
            self.estado_atual = self._estados[27]

            if erro_estado_inicial:
                return True, entrada, ErrosLexicos.CARACTERE_INVALIDO.value
            else:
                return True, self.caminho_percorrido, ErrosLexicos.LEXEMA_MAL_FORMADO.value

        return True, self.caminho_percorrido, None

    def caractere_para_entrada(self, caractere):
        if caractere in self.ALFABETO_LETRAS:
            if self.estado_atual in [self._estados[1], self._estados[3]] and caractere in ['E', 'e']:
                return caractere
            return ClassesEntrada.LETRA.value
        if caractere in self.ALFABETO_DIGITOS:
            return ClassesEntrada.DIGITO.value
        if caractere in self.ALFABETO_IGNORAR:
            return ClassesEntrada.IGNORAR.value
        if caractere in self.ALFABETO_EOF:
            return ClassesEntrada.EOF.value
        
        return caractere

    def volta_inicio(self):
        self.estado_atual = self._estados[0]
        self.caminho_percorrido = ""