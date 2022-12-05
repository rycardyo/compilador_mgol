import sys

from tabelaSimbolos import tabelaSimbolos
from tokenLexico import Classes, Token
from scanner import SCANNER


def main():
  caminho_arquivo: str = sys.argv[1]
  arquivo = open(caminho_arquivo, 'r')

  token: Token = SCANNER(arquivo)
  print("Token reconhecido", token)
  while token['classe'] != Classes.EOF.value:
    token = SCANNER(arquivo)
    print("Token reconhecido", token)

  print("saiu", token['classe']), 
  arquivo.close()

main()