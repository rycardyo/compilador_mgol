# Versao python : 3.10

import sys
from tokenLexico import Classes, Token
from scanner import SCANNER
from os.path import realpath, dirname


def main():
  caminho_arquivo: str = '{path}/teste.txt'.format(path=dirname(realpath(__file__)))
  arquivo = open(caminho_arquivo, 'r')

  token: Token = SCANNER(arquivo)
  print("Token reconhecido", token)
  while token['classe'] != Classes.EOF.value:
    token = SCANNER(arquivo)
    print("Token reconhecido", token)

  print("saiu", token['classe']), 
  arquivo.close()

main()