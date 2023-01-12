from enum import Enum
from typing import Optional, TypedDict

class Classes(Enum):
  NUM = "NUM"
  LIT = "LIT"
  ID = "ID"
  COMENTARIO = "COMENTARIO"
  OPR = "OPR"
  ATR = "ATR"
  OPA = "OPA"
  AB_P = "AB_P"
  FC_P = "FC_P"
  PT_V = "PT_V"
  VIR = "VIR"
  ERRO = "ERRO"
  EOF = "EOF"
  NONE = None

class Tipos(Enum):
  INTEIRO = "INTEIRO"
  REAL = "REAL"
  LITERAL = "LITERAL"
  NONE = None

class Token(TypedDict):
  classe: Classes
  lexema: str
  tipo: Optional[Tipos]