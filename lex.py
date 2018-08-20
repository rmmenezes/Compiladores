import ply.lex as lex

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'then' : 'THEN',
    'while' : 'WHILE',
    'print' : 'PRINT'
}

tokens = ['ID',
          'DOIS_PONTOS',
          'ATRIBUICAO',
          'MENOR',
          'MAIOR',
          'MULT',
          'VIRGULA',
          'SOMA',
          'MENOS',
          'INT',
          'FLOAT',
          'DIVIDE',
          'ABREPAREN',
          'FECHAPAREN'

          ] + list(reserved.values())

t_ignore = r' \t'


t_DOIS_PONTOS = r':'
t_VIRGULA = r','

##operadores
t_SOMA = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'

##simbolos
t_ABREPAREN = r'\('
t_FECHAPAREN = r'\)'
t_MENOR = r'<'
t_MAIOR = r'>'
t_ATRIBUICAO = r':='

t_INT= r'[+-]?[0-9]+'
t_FLOAT = r'[+-]?[0-9]*\?[0-9]+'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_error(t):
    print("Erro", t.value)
    t.lexer.skip(1)

lex.lex();


lex.input("rafael menezes(print)+1 if else then IF")
while True:
    tok = lex.token()
    if not tok: break
    print(tok)
