from tabelaSimbolos import tabelaSimbolos
from tokenLexico import Classes

print(tabelaSimbolos.buscar("meu"))
tabelaSimbolos.inserir({"classe": Classes.ID.value, "lexema": "meu", "tipo": None})
tabelaSimbolos.atualizar({"classe": Classes.AB_P.value, "lexema": "meu", "tipo": None})
print(tabelaSimbolos.buscar("meu"))
