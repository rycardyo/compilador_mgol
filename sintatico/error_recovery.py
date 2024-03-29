import sys
from os.path import realpath, dirname

path = '{path}/../lexico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

from mapaTransicoes import Acoes, MapaTransicoes
import copy 
from pilha import Pilha
from scanner import SCANNER
from enchant import utils
import numpy as np
import afd
from tokenLexico import Classes
from tabelaSimbolos import tabelaSimbolos

class Recovery():   
    def __init__(self, parser_stack : Pilha, token : str, scanner : SCANNER,
                                arquivo, mapaTransicoes : MapaTransicoes, posicao : tuple, posicao_ultimo_erro : tuple,
                                caminho_arquivo : str, map_tokens : dict ) -> None:
        self.map_tokens = map_tokens
        self.parser_stack = parser_stack
        self.token = token
        self.scanner = scanner
        self.arquivo = arquivo
        self.mapaTransicoes = mapaTransicoes
        self.estado_erro = mapaTransicoes.shiftReduceError[self.parser_stack.topo()]
        self.new_file = open(caminho_arquivo, "r").readlines()
        self.linha, self.coluna = posicao
        self.terminais_candidatos = [x for x in self.estado_erro if self.estado_erro[x]['acao'].value != Acoes.ERROR.value]  
        self.distance = 2
        self.posicao = posicao
        self.imprime = posicao != posicao_ultimo_erro
        self.gera_cadeia()
        self.recovery_token = self.local_recovery()
        
        if self.recovery_token == 0: 
            self.recovery_token = self.panic_mode()


    def gera_cadeia(self):
        arq = copy.deepcopy(self.new_file)
        arq = arq[self.linha - 1:]
        arq = ''.join(arq)
        arq = arq[self.coluna - 1:]
        self.cadeia = arq


    def panic_mode(self):
        _token = self.token
        cont = 0
        while _token['classe'] != '$':
            recovery_stack = copy.deepcopy(self.parser_stack)
            entrada = _token['classe']
            if entrada != 'ERRO':
                while recovery_stack.len() > 0:
                    estadoAtual = recovery_stack.topo()
                    acao = self.mapaTransicoes.shiftReduceError[estadoAtual][entrada]['acao']
                    if acao.value != Acoes.ERROR.value:
                        # retorno pode ser o scanner, necessario testar
                        self.parser_stack = recovery_stack
                        return _token, self.parser_stack
                    cont = cont + 1
                    recovery_stack.remover()
                # avaliar variaveis globais da classe (scanner e arquivo)    
            _token = self.scanner(self.arquivo)[0]
        return None,None


    def local_recovery(self):
        # minimal distance = 2
        distance = 2

        acoes = [self.concatena, self.remove_token, self.insere_terminal_antes, self.substitui_por_terminal]

        ok = False
        for acao in acoes:
            result = acao()
            if result[0] != 0:
                ok = True
                break
            else:
                continue
        if ok:
            return self.run_local_recovery(result)
        else:
            return 0


    def run_local_recovery(self, chosen_action):
        id_action = chosen_action[1]
        token_action = chosen_action[0]
        if id_action == 0:
            if self.imprime:
                token_mensagem = self.map_tokens[token_action['classe']] if token_action['classe'] in self.map_tokens else token_action['classe'] 
                print('Era esperado: "{}"'.format(token_mensagem))
            return token_action, self.parser_stack
        
        elif id_action == 1:
            self.scanner(self.arquivo)
            if self.imprime:
                token_mensagem = self.map_tokens[token_action['classe']] if token_action['classe'] in self.map_tokens else token_action['classe']                 
                print('O token "{}" não era esperado'.format(token_mensagem))
            
            return token_action, self.parser_stack
        
        elif id_action == 2:
            new_token = self.altera_pilha(token_action['classe'])
            if self.imprime:
                token_mensagem = self.map_tokens[token_action['classe']] if token_action['classe'] in self.map_tokens else token_action['classe']                 
                token_mensagem_2 = self.map_tokens[self.token['classe']] if self.token['classe'] in self.map_tokens else self.token['classe']                  

                print('Era esperado o token "{}" antes de "{}"'.format(token_mensagem, token_mensagem_2))
            return new_token, self.parser_stack
        
        elif id_action == 3:
            if self.imprime:
                token_mensagem = self.map_tokens[token_action['classe']] if token_action['classe'] in self.map_tokens else token_action['classe']                 
                token_mensagem_2 = self.map_tokens[self.token['classe']] if self.token['classe'] in self.map_tokens else self.token['classe']                 

                print('Era esperado o token "{}" ao inves de "{}"'.format(token_mensagem, token_mensagem_2))
            return token_action, self.parser_stack
     

    def scanner_lexema(self, cadeia):
        lexema = ''
        _afd = afd.AFD()
        for c in cadeia:
            afd_parou, lexema, _ = _afd.transicao(c)
            if afd_parou:
                break

        token = { 
            "classe": _afd.estado_atual.token_class.value,
            "lexema": lexema,
            "tipo": _afd.estado_atual.token_type.value,
            }
        if token["classe"] == Classes.ID.value:
            token_existente = tabelaSimbolos.buscar(lexema)
            if token_existente != None:
                token = token_existente

        return token


    def altera_pilha(self, token : str) -> dict:
        estado_atual = self.mapaTransicoes.shiftReduceError[self.parser_stack.topo()][token]
        new_token = {'classe' : '', 'lexema' : ''}      

        if estado_atual["acao"].value == Acoes.SHIFT.value:
            self.parser_stack.inserir(estado_atual["estado"])
            new_token = self.token
            return new_token
        
        elif estado_atual["acao"].value == Acoes.REDUCE.value:
        
            for estadoEmpilhado in estado_atual["direita"]:
                self.parser_stack.remover()
        
            self.parser_stack.inserir(self.mapaTransicoes.goto[self.parser_stack.topo()][estado_atual["esquerda"]])
            new_token['classe'] = token
            new_token = self.altera_pilha(new_token['classe'])
      
        return new_token

    def minimal_distance(self, limite : int, token : str, cadeia : str ,tipo : str = 'remocao') -> int:
        recovery_stack = copy.deepcopy(self.parser_stack)
        entrada = token
        cadeia = copy.deepcopy(cadeia)
        cont = 0 if tipo == 'remocao' else -1   
        
        while cont <= limite and entrada != 'ERRO' and entrada != None:
            estado_atual = self.mapaTransicoes.shiftReduceError[recovery_stack.topo()][entrada]
            
            if estado_atual["acao"].value == Acoes.SHIFT.value:

                recovery_stack.inserir(estado_atual["estado"])
                token = self.scanner_lexema(cadeia) 
                entrada = token['classe']
                cadeia = cadeia[len(token['lexema']):]    
                cont = cont + 1

            elif estado_atual["acao"].value == Acoes.REDUCE.value:

                for estadoEmpilhado in estado_atual["direita"]:
                    recovery_stack.remover()
                
                recovery_stack.inserir(self.mapaTransicoes.goto[recovery_stack.topo()][estado_atual["esquerda"]])
                cont = cont + 1
            
            elif estado_atual["acao"].value == Acoes.ACCEPT.value:
                return limite                    
            
            else:
                return cont
     
        return cont


    # Mescla o token atual como proximo e calcula minimal distance
    # Verificar se faz sentido...
    def testa_candidatos(self, candidatos : list, tipo_teste = 'remocao'):
        candidatos_aceitos = []
        levenshtein = []
        cadeia_base = copy.deepcopy(self.cadeia)
        cadeia = self.token['lexema'] + ' ' + cadeia_base if tipo_teste != 'remocao' else cadeia_base
       
        for item in candidatos:
            score = self.minimal_distance(self.distance, item, tipo = tipo_teste, cadeia =cadeia)
     
            if score >= self.distance:
                candidatos_aceitos.append(item)
                levenshtein.append(utils.levenshtein(item, self.token))
     
        if len(candidatos_aceitos) > 0:
            _token = {
                'classe' : candidatos_aceitos[np.argmin(levenshtein)],
                'lexema' : ''}
            return _token
        
        else:
            return 0

    # Nao utilizada
    def concatena(self) -> tuple:
        id_action = 0
        t1 = self.token["lexema"]
        cadeia = copy.deepcopy(self.cadeia)
        t2 = self.scanner_lexema(cadeia)['lexema']
        cadeia = cadeia[len(t2):]
        if len(t2) > 0:
            token_concat = t1 + t2
            new_token = self.scanner_lexema(token_concat)
            
            if new_token['classe'] != "ERRO": 
                custo = self.minimal_distance(self.distance, new_token['classe'], tipo = 'remocao', cadeia = cadeia) 
                if custo >= self.distance:
                    return (new_token, id_action)
                else:
                    return (0,id_action)
            else:
                return (0,id_action)
        else:
            return (0,id_action)


    # Remove o token atual e verifica se o parser aceita
    def remove_token(self) -> tuple: 
        entrada = 0
        id_action = 1
        cadeia = copy.deepcopy(self.cadeia)
        next_token = self.scanner_lexema(cadeia) 
        entrada = 0
     
        if next_token['classe'] != "ERRO" and  next_token['classe'] !=  None:
            score = self.minimal_distance(self.distance, next_token['classe'], cadeia=cadeia)
     
            if score >= self.distance:
                entrada = next_token
     
        return entrada, id_action
        

    # Inserir cada candidato terminal antes o simbolo atual
    def insere_terminal_antes(self) -> tuple:
        id_action = 2
        token_provavel = self.testa_candidatos(self.terminais_candidatos, 'insercao')
       
        return (token_provavel,id_action)
         

    # substituir atual por cada candidato terminal        
    def substitui_por_terminal(self) -> tuple:
        id_action = 3
     
        return (self.testa_candidatos(self.terminais_candidatos, 'remocao'), id_action)
    

   
    