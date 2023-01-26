import sys
from os.path import realpath, dirname

path = '{path}/../lexico'.format(path=dirname(realpath(__file__)))
sys.path.insert(0, path)

from mapaTransicoes import Acoes
import copy 
from pilha import Pilha
from scanner import SCANNER
from enchant import utils
import numpy as np
import afd

class Recovery():   
    def __init__(self, parser_stack : Pilha, token : str, scanner : SCANNER,
                                arquivo, mapaTransicoes : dict, posicao : tuple, posicao_ultimo_erro : tuple ) -> None:
        self.parser_stack = parser_stack
        self.token = token
        self.scanner = scanner
        self.arquivo = arquivo
        self.mapaTransicoes = mapaTransicoes
        self.estado_erro = mapaTransicoes.shiftReduceError[self.parser_stack.topo()]
        
        self.terminais_candidatos = [x for x in self.estado_erro if self.estado_erro[x]['acao'].value != Acoes.ERROR.value]  
        self.distance = 2
        self.imprime = posicao != posicao_ultimo_erro
        self.recovery_token = self.local_recovery()
        if self.recovery_token == 0: 
            print('local_falhou')
            self.recovery_token = self.panic_mode()
    

    def panic_mode(self):
        _token = self.token
        cont = 0
        while _token['classe'] != '$':
            recovery_stack = copy.deepcopy(self.parser_stack)
            entrada = _token['classe']
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

        acoes = [self.concatena,self.remove_token, self.insere_terminal_antes, self.substitui_por_terminal]

        ok = False
        cont = 0
        for acao in acoes:
            print('testando regra {}'.format(cont))
            cont = cont + 1
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
        print("Regra escolhida : {}".format(id_action))
        if id_action == 0:
            if self.imprime:
                print('Era esperado: {}'.format(token_action))
            return token_action, self.parser_stack
        
        elif id_action == 1:
            self.scanner(self.arquivo)[0]
            if self.imprime:
                print('O token {} não era esperado'.format(token_action))
            return token_action, self.parser_stack
        
        elif id_action == 2:
            new_token = self.altera_pilha(token_action['classe'])
            if self.imprime:
                print('Era esperado o token {} antes de {}'.format(token_action, self.token))
            return new_token, self.parser_stack
        
        elif id_action == 3:
            if self.imprime:
                print('Era esperado o token {} ao inves de {}'.format(token_action, self.token))
            return token_action, self.parser_stack
     

    def altera_pilha(self, token : str) -> dict:
        estado_atual = self.mapaTransicoes.shiftReduceError[self.parser_stack.topo()][token]
        new_token = {'classe' : '', 'lexema' : ''}        
        if estado_atual["acao"].value == Acoes.SHIFT.value:
            self.parser_stack.inserir(estado_atual["estado"])
          
            new_token['classe'] = self.token['classe']

        elif estado_atual["acao"].value == Acoes.REDUCE.value:
            for estadoEmpilhado in estado_atual["direita"]:
                self.parser_stack.remover()
            self.parser_stack.inserir(self.mapaTransicoes.goto[self.parser_stack.topo()][estado_atual["esquerda"]])
            new_token['classe'] = token
        return new_token

    def minimal_distance(self, limite : int, token : str, tipo : str = 'remocao', scan : SCANNER = None) -> int:
        copy_scan = copy.deepcopy(self.scanner) if scan == None else scan
        recovery_stack = copy.deepcopy(self.parser_stack)
        entrada = token
        cont = 0 if tipo == 'remocao' else -1   
        
        while cont <= limite:
            estado_atual = self.mapaTransicoes.shiftReduceError[recovery_stack.topo()][entrada]
            if estado_atual["acao"].value == Acoes.SHIFT.value:
                recovery_stack.inserir(estado_atual["estado"])
                entrada = copy_scan(self.arquivo)[0]['classe'] if cont > 0 else self.token['classe']
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
        for item in candidatos:
            if self.minimal_distance(self.distance, item, tipo = tipo_teste) >= self.distance:
                candidatos_aceitos.append(item)
                levenshtein.append(utils.levenshtein(item, self.token))
       
        if len(candidatos_aceitos) > 0:
            _token = {'classe' : candidatos_aceitos[np.argmin(levenshtein)],
                    'lexema' : ''}
            return _token
        else:
            return 0

    # Nao utilizada
    def concatena(self):
        id_action = 0
        copy_scan = copy.deepcopy(self.scanner)
        
        t1 = self.token["lexema"]
        t2 = copy_scan(self.arquivo)[0]["lexema"]
        if len(t2) > 0:
            _afd = afd.AFD()
            token_concat = t1 + t2
            lexema = ''
            for c in token_concat:
                _, lexema, _ = _afd.transicao(c)

            token_concat = { 
                "classe": _afd.estado_atual.token_class.value,
                "lexema": lexema,
                "tipo": _afd.estado_atual.token_type.value,
                }
            if token_concat['classe'] != "ERRO": 
                custo = self.minimal_distance(self.distance, token_concat['classe'], tipo = 'remocao', scan = copy_scan) 
                print('teste r1 realizado')
                if custo >= self.distance:
                    return (token_concat, id_action)
                else:
                    return (0,id_action)
            else:
                return (0,id_action)
        else:
            return (0,id_action)

    # Remove o token atual e verifica se o parser aceita
    def remove_token(self) -> tuple: 
        id_action = 1
        recovery_stack = copy.deepcopy(self.parser_stack)
        _token, posicao = SCANNER(self.arquivo)
        entrada = 0
        print('PROXIMO TOKEN {}'.format(_token)) 
        print(posicao)
        score = self.minimal_distance(self.distance, _token['classe'])
        print('PROXIMO TOKEN {}'.format(_token)) 
        if score >= self.distance:
            entrada = _token
        
        return (entrada, id_action)

    # Inserir cada candidato terminal antes o simbolo atual
    def insere_terminal_antes(self) -> tuple:
        id_action = 2
        token_provavel = self.testa_candidatos(self.terminais_candidatos, 'insercao')
        return (token_provavel,id_action)
         

    # substituir atual por cada candidato terminal        
    def substitui_por_terminal(self) -> tuple:
        id_action = 3
        return (self.testa_candidatos(self.terminais_candidatos, 'remocao'), id_action)
    

   
    