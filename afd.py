from typing import Dict
import tokenLexico as token

class estado():
    def __init__(self, id: int, final:bool = False, token_class: token.Classes = token.Classes.ERRO, token_type : token.Tipos = None) -> None:
        self.id = id

    #transicoes dict[str, estado]
    def gera_transicao(self, transicoes : dict) -> None:
        self.transicoes = transicoes


    def is_final(self, token_class: token.Classes, token_type: token.Tipos = None) -> None:
        self.final = True 
        self.token_class = token_class
        self.token_type = token_type


class afd():
    _estados : list
    _tabela_transicoes: Dict[str, dict]

    def gera_transicoes(self, entradas: list, id_estado_atual: str, id_destino: str) -> None:
        _transicoes = self._tabela_transicoes[id_estado_atual]
        for item in entradas:
            _transicoes[item] = self._estados[int(id_destino)]
        
        self._tabela_transicoes[id_estado_atual] = _transicoes


    def gera_tabela_transicoes(self) -> None:
        self._tabela_transicoes = {str(estado.id) : {} for estado in self._estados}
        

        # Estado 0
        estado_atual = '0'
        self.gera_transicoes(self.ALFABETO_DIGITOS, estado_atual,'1')
        self.gera_transicoes(self.ALFABETO_LETRAS, estado_atual,'7')
        self.gera_transicoes(['"'], estado_atual, '8')
        self.gera_transicoes(["{"], estado_atual, '11')
        self.gera_transicoes(["EOF"], estado_atual, '14')
        self.gera_transicoes([">"], estado_atual, '15')
        self.gera_transicoes(["<"], estado_atual, '17')
        self.gera_transicoes(["="], estado_atual, '21')
        self.gera_transicoes(["/","*","-","+"], estado_atual, '22')
        self.gera_transicoes([","], estado_atual, '23')
        self.gera_transicoes([";"], estado_atual, '24')
        self.gera_transicoes(["("], estado_atual, '25')
        self.gera_transicoes([")"], estado_atual, '26')
        # O ERRO PODE SER GERADO A PARTIR DA EXCEPTION KEYERROR...  
        
        # Estado 01
        estado_atual = '1'
        self.gera_transicoes(self.ALFABETO_DIGITOS, estado_atual, estado_atual)
        self.gera_transicoes(["."], estado_atual, '2')
        self.gera_transicoes(["e","E"], estado_atual, '4')

        # Estado 02
        estado_atual = '2'
        self.gera_transicoes(self.ALFABETO_DIGITOS, estado_atual, '3')

        # Estado 03
        estado_atual = '3'
        self.gera_transicoes(["e","E"], estado_atual, '4')
        
        # Estado 04
        estado_atual = '4'
        self.gera_transicoes(['+','-'], estado_atual, '5')
        self.gera_transicoes(self.ALFABETO_DIGITOS, estado_atual, '6')                                

        # Estado 05
        estado_atual = '5'
        self.gera_transicoes(self.ALFABETO_DIGITOS, estado_atual, '6')

        # Estado 06
        estado_atual = '6'
        self.gera_transicoes(self.ALFABETO_DIGITOS, estado_atual, estado_atual)

        # Estado 07
        estado_atual = '7'
        self.gera_transicoes(self.ALFABETO_DIGITOS + self.ALFABETO_LETRAS + ['_'], estado_atual, estado_atual)

        # Estado 08
        estado_atual = '8'
        self.gera_transicoes(self.ALFABETO, estado_atual, '9')

        # Estado 09
        estado_atual = '9'
        self.gera_transicoes(self.ALFABETO, estado_atual, estado_atual)
        self.gera_transicoes(['"'], estado_atual, '10')

        # Estado 10
        # Estado final sem transições
        
        # Estado 11
        estado_atual = '11'
        self.gera_transicoes(self.ALFABETO, estado_atual, '12')

        # Estado 12
        estado_atual = '12'
        self.gera_transicoes(self.ALFABETO, estado_atual, estado_atual)
        self.gera_transicoes(['}'], estado_atual, '13')

        # Estado 13
        # Estado final sem transições

        # Estado 14
        # Estado final sem transições

        # Estado 15
        estado_atual = '15'
        self.gera_transicoes(['='], estado_atual, '16')

        # Estado 16
        # Estado final sem transições

        # Estado 17
        estado_atual = '17'
        self.gera_transicoes(['='],estado_atual, '18')
        self.gera_transicoes(['<'],estado_atual, '19')
        self.gera_transicoes(['-'], estado_atual, '20')

        # Estado 18
        # Estado final sem transicoes

        # Estado 19
        # Estado final sem transicoes

        # Estado 20
        # Estado final sem transicoes

        # Estado 21
        # Estado final sem transicoes
        
        # Estado 22
        # Estado final sem transicoes

        # Estado 23
        # Estado final sem transicoes

        # Estado 24
        # Estado final sem transicoes

        # Estado 25
        # Estado final sem transicoes

        # Estado 26
        # Estado final sem transicoes

        # Estado 27
        # Estado final sem transicoes        
        

    def transicao(self, idx_estado: int, entrada : str) -> estado:
        try:
            return self._estados[idx_estado].transicoes[entrada]
        except KeyError: 
            # Retorna estado de erro
            return self._estados[-1]    

    def __init__(self, qntd__estados: int) -> None:
            
        
        self.ALFABETO_LETRAS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.ALFABETO_LETRAS = self.ALFABETO_LETRAS + [x.upper() for x in self.ALFABETO_LETRAS]
        self.ALFABETO_DIGITOS = [x for x in range(10)]
        self.ALFABETO_DEMAIS_CARACTERS = [',', ';', ':', '.', '!', '?', '\\', '*', '+', '-', '/', '(', ')', '{', '}', '[',']', '<', '>', '=', "‘", '“']
        self.ALFABETO = self.ALFABETO_DIGITOS + self.ALFABETO_LETRAS + self.ALFABETO_DEMAIS_CARACTERS
        
        # Criando os _estados
        self._estados = [estado(id = i) for i in range(qntd__estados)]

        # Definindo os _estados finais 
        
        # Numericos
        self._estados[1].is_final(token.Classes.NUM, token.Tipos.INTEIRO)
        self._estados[3].is_final(token.Classes.NUM, token.Tipos.REAL)
        self._estados[6].is_final(token.Classes.NUM, token.Tipos.REAL)

        # Ids
        # Os tipos do id deveram ser definidos com auxilio das palavras reservadas INTEIRO, REAL, etc
        self._estados[7].is_final(token.Classes.ID)

        # Literal
        self._estados[10].is_final(token.Classes.LIT, token.Tipos.LITERAL)

        # Comentario
        self._estados[13].is_final(token.Classes.COMENTARIO)

        # EOF
        self._estados[14].is_final(token.Classes.EOF)

        # OPRs 
        self._estados[15].is_final(token.Classes.OPR)
        self._estados[16].is_final(token.Classes.OPR)
        self._estados[17].is_final(token.Classes.OPR)
        self._estados[18].is_final(token.Classes.OPR)
        self._estados[19].is_final(token.Classes.OPR)
        self._estados[21].is_final(token.Classes.OPR)

        #Atr
        self._estados[20].is_final(token.Classes.ATR)

        # OPA
        self._estados[22].is_final(token.Classes.OPA)

        # VIR
        self._estados[23].is_final(token.Classes.VIR)

        # PT_V
        self._estados[24].is_final(token.Classes.PT_V)

        # AB_P
        self._estados[25].is_final(token.Classes.AB_P)

        # FC_P
        self._estados[26].is_final(token.Classes.ATR)

        # ERRO
        self._estados[27].is_final(token.Classes.ERRO)

        # Gera a tabela de transicoes
        self.gera_tabela_transicoes()

        # Define as transicoes de cada estado 
        
        # Uma alternativa seria nao utiliza as transições de cada estado mas a propria tabela de transicoes dentro do scanner
        for idx, _ in enumerate(self._estados):
            self._estados[idx].gera_transicao(self._tabela_transicoes[str(self._estados[idx].id)])

        
        del self._tabela_transicoes

    # Pseudo algoritmo do scanner
    '''
        estado_atual = estado_0
        for char in input:
            if estado_atual.possui_transicoes:
                estado_atual = estado_atual.transicao[char]
            else:
                break
            # Onde a possui_transicoes pode ser um dos atributos do estado do automato que indica se o mesmo possui ou não transicoes 
            # Ao inves disso posso tentar somente retornar um break na funcao de transicoes do estado quando ele nao as possuir  
    '''

automato = afd(28)
print(automato._estados[0].transicoes)