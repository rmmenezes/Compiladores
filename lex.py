import sys
import ply.lex as lex

RESERVED = {
          'se': 'SE',
          'senão':'SENAO',
          'então':'ENTAO',
          'repita':'REPITA',
          'escreva':'ESCREVA',
          'leia':'LEIA',
          'até':'ATE',
          'fim':'FIM',
          'inteiro' : 'INTEIRO',
          'flutuante' : 'FLUTUANTE',
          'retorna' : 'RETORNA',
}

tokens = ['ID',
          'DOIS_PONTOS',
          'ATRIBUICAO',
          'MENOR',
          'MAIOR',
          'MENOR_IGUAL',
          'MAIOR_IGUAL',
          'MULT',
          'VIRGULA',
          'MAIS',
          'MENOS',
          'DIVIDE',
          'ABRE_PAREN',
          'FECHA_PAREN',
          'ABRE_COUCH',
          'FECHA_COUCH',
          'SE',
          'SENAO',
          'ENTAO',
          'REPITA',
          'ESCREVA',
          'LEIA',
          'ATE',
          'FIM',
          'INTEIRO',
          'FLUTUANTE',
          'COMPARACAO',
          'NUMERO',
          'RETORNA',
          'E_LOGICO',
          'OU_LOGICO',
          'NEGACAO',
          'QUEBRA_LINHA',
          ]

t_ignore = " \t\n"

##operadores
t_MAIS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_COMPARACAO = r'='

##simbolos
t_ABRE_PAREN = r'\('
t_FECHA_PAREN = r'\)'
t_ABRE_COUCH = r'\['
t_FECHA_COUCH = r'\]'
t_MENOR = r'<'
t_MAIOR = r'>'
t_ATRIBUICAO = r':='
t_MENOR_IGUAL = r'<='
t_MAIOR_IGUAL = r'>='

##operadores logicos
t_E_LOGICO = r'&&'
t_OU_LOGICO = r'\|\|'
t_NEGACAO = r'!'

##pontuação
t_DOIS_PONTOS = r':'
t_VIRGULA = r','

t_NUMERO = r'([0-9]+)(\.[0-9]+)?([e|E][+|-]?[0-9]+)?'


def t_ID(t):
    r'[A-Za-z_][\w]*'
    t.type = RESERVED.get(t.value, 'ID')
    return t

def t_comment(t):
    r'\{[^}]*[^{]*\}'
    pass

def t_error(t):
    print("Erro", t.value[0])
    raise SyntaxError("ERRO", t.value[0])
    t.lexer.skip(1)

lex.lex()

file = open(sys.argv[1], "r", encoding="utf-8")

lex.input(file.read())
while True:
    tok = lex.token()
    if not tok: break
    print( tok.type, ':', tok.value )
