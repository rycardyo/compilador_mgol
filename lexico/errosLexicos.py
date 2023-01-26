from enum import Enum


class ErrosLexicos(Enum):
  CARACTERE_INVALIDO = 1
  LEXEMA_MAL_FORMADO = 2
  LITERAL_INCOMPLETA = 3
  COMENTARIO_INCOMPLETO = 4