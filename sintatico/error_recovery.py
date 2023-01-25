import sys
from os.path import realpath, dirname

path = '{path}/../lexico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

from mapaTransicoes import MapaTransicoes, Acoes
import copy 
from pilha import Pilha
from scanner import SCANNER
from enchant import utils
import numpy as np

class Recovery():   
    def __init__(self, parser_stack : Pilha, token : str, scanner : SCANNER,
                                arquivo, mapaTransicoes : dict) -> None:
        self.parser_stack = parser_stack
        self.token = token
        self.scanner = scanner
        self.arquivo = arquivo
        self.mapaTransicoes = mapaTransicoes
        self.estado_erro = mapaTransicoes.shiftReduceError[self.parser_stack.topo()]
        self.tokens_candidatos = self.estado_erro['codigo']
        self.panic_mode(self.token)
    
    def local_recovery(self, token : str, parser_stack : Pilha):
        # minimal distance = 2
        distance = 2
        self.token = token

        acoes = [self.concatena, self.remove_token, self.insere_terminal_antes, 
                    self.substitui_por_terminal, self.insere_nao_terminal_antes, self.substitui_por_nao_terminal]

        mapeia_acoes = {
            0 : 'concat',
            1 : 'remove',
            2 : 'insere_terminal',
            3 : 'substitui_por_terminal',
            4 : 'insere_nao_terminal',
            5 : 'substitui por nao_terminal'
        }        
        for acao in acoes:
            result = acao()
            if result[0] >= distance:
                acao_realizada = result[1]
                break
        print(acao_realizada)

        def minimal_distance(self, value : int, token : str, tipo : str = 'remocao', scan : SCANNER = None) -> int:
            copy_scan = copy.deepcopy(self.scanner) if scan == None else scan
            recovery_stack = copy.deepcopy(parser_stack)
            entrada = token
            cont = 0 if tipo == 'remocao' else -1   
            while cont <= value:
                estado_atual = recovery_stack.topo()
                acao = self.mapaTransicoes.shiftReduceError[estado_atual][entrada]['acao']
                if acao.value != Acoes.ERROR.value:
                    cont = cont + 1
                    entrada = copy_scan()['classe'] if cont > 0 else self.token
                else:
                    return cont
            return cont


       # Mescla o token atual como proximo e calcula minimal distance
       # Verificar se faz sentido...
        def testa_candidatos(self, candidatos : list, tipo_teste = 'remocao'):
            candidatos_aceitos = []
            levenshtein = []
            for item in candidatos:
                if self.minimal_distance(distance, item, tipo = tipo_teste) >= distance:
                    candidatos_aceitos.append(item)
                    levenshtein.append(utils.levenshtein(item, self.token))
            if len(candidatos_aceitos) > 0:
                return candidatos_aceitos[np.argmax(levenshtein)]
            else:
                return 0

        # Nao utilizada
        def concatena(self):
            id_action = 0
            copy_scan = copy.deepcopy(self.scanner)
            t1 = token["lexema"]
            t2 = copy_scan()["lexema"]
            token_concat = t1 + t2
            
            return (self.minimal_distance(distance, token_concat, tipo = 'remocao', scan = copy_scan), id_action)

        # Remove o token atual e verifica se o parser aceita
        def remove_token(self) -> tuple: 
            id_action = 1
            recovery_stack = copy.deepcopy(parser_stack)
            token = copy.deepcopy(self.scanner)
            entrada = token['classe']
            
            return (self.minimal_distance(distance, entrada), id_action)

        # Inserir cada candidato terminal antes o simbolo atual
        def insere_terminal_antes(self) -> tuple:
            id_action = 2
            return (testa_candidatos(self.tokens_candidatos, 'insercao'), id_action)

        # substituir atual por cada candidato terminal        
        def substitui_por_terminal(self) -> tuple:
            id_action = 3
            return (self.testa_candidatos(self.tokens_candidatos, 'remocao'), id_action)
        
        # inserção de nao terminais antes
        def insere_nao_terminal_antes(self) -> tuple:
            id_action = 4
            return (testa_candidatos(self.tokens_candidatos, 'insercao'), id_action)

        # Substituir um candidato nao terminal por t1
        def substitui_por_nao_terminal(self) -> tuple:
           id_action = 5
           return (self.testa_candidatos(self.tokens_candidatos, 'remocao'), id_action)


    
    # pendencias: escrever tipagem
    # verificar ancoras
    
    def panic_mode(self,token):
        print('Token que disparou o erro: {}'.format(token))
        while token['classe'] != '$':
            print('Token Atual: {}'.format(token))
            recovery_stack = copy.deepcopy(self.parser_stack)
            print('Pilha: {}'.format(recovery_stack.len()))
            entrada = token['classe']
            while recovery_stack.len() > 0:
                estadoAtual = recovery_stack.topo()
                print('Estado no topo: {}'.format(estadoAtual))
                acao = self.mapaTransicoes.shiftReduceError[estadoAtual][entrada]['acao']
                print('AÇÃO: {}'.format(acao.value))
                if acao.value != Acoes.ERROR.value:
                    # retorno pode ser o scanner, necessario testar
                    return recovery_stack, token
                recovery_stack.remover()
            # avaliar variaveis globais da classe (scanner e arquivo)    
            token = self.scanner(self.arquivo)
        return None, None

    