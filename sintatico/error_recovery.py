from mapaTransicoes import MapaTransicoes, Acoes
import copy 
class recovery():   
    def __init__(self, parser_stack, token, scanner, arquivo, mapaTransicoes):
        self.parser_stack = parser_stack
        self.token = token
        self.scanner = scanner
        self.arquivo = arquivo
        self.mapaTransicoes = mapaTransicoes
         

    def local_recovery(self, token):
        return 0 
    
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
                    return recovery_stack, self.scanner
                recovery_stack.remover()
            # avaliar variaveis globais da classe (scanner e arquivo)    
            token = self.scanner(self.arquivo)
        return None, None

    