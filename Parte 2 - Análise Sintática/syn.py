import ply.yacc as yacc
from lex import Lexer

def __init__(self, type_node='', child=[], value=''):
    self.type = type_node
    self.child = child
    self.value = value

def p_programa(p):
    'programa : lista_declaracoes'
    p[0] =  Tree('programa', [p[1]])

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                        | declaracao'''
    if len(p) == 3:
        p[0] = Tree('lista_declaracoes', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Tree('lista_declaracoes', [p[1]])

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
                    | inicializacao_variaveis
                    | declaracao_funcao '''
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
    p[0] = Tree('declaracao_variaveis', [p[1]])


def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''
    p[0] = Tree('inicializacao_variaveis', [p[1]])

def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var
                        | var '''
    if len(p) == 4:
        p[0] = Tree('lista_variaveis', [p[1], p[3]])
    elif len(p) == 2:
        p[0] = Tree('lista_variaveis', [p[1]])

def p_var(p):
    ''' var : ID
            | ID indice '''
    if len(p) == 2:
        p[0] =  Tree('var', [p[1]])
    elif len(p) == 3:
        ##DAR UMA OLHADA NESTE SEGUNDO PARAMETRO
        p[0] = Tree('var', [p[2]], p[1])

def p_indice(p):
    ''' indice : indice ABRE_COUCH expressao FECHA_COUCH
                | ABRE_COUCH expressao FECHA_COUCH '''
    if len(p) == 5:
            p[0] = Tree('indice', [p[1], p[3]])
    elif len(p) == 4:
            p[0] = Tree('indice', [p[2]])


def p_tipo(p):
    ''' tipo : INTEIRO
            | FLUTUANTE '''
    p[0] = Tree('tipo', [p[1]])

def p_declaracao_funcao(p):
    ''' declaracao_funcao : tipo cabecalho
                            | cabecalho  '''
    if len(p) == 3:
        p[0] = Tree('declaracao_funcao', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Tree('declaracao_funcao', [p[1]])

##DAR UMA OLHADA SE NAO PRECISA DE MAIS COISAS AQUI
def p_cabecalho(p):
    ''' cabecalho : ID ABRE_PAREN lista_parametros FECHA_PAREN corpo FIM '''
    p[0] = Tree('cabecalho', [[p[3], p[5]], p[1]])

def p_lista_parametros(p):
    ''' lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio '''
    if len(p) == 4:
        p[0] =  Tree('lista_parametros', [p[1], p[3]])
    elif len(p) == 2:
        p[0] =  Tree('lista_parametros', [p[1]])

##VER SE NAO FALTA ALGUMA COISA
def p_parametro(p):
    ''' parametro : tipo DOIS_PONTOS ID
                    |  parametro ABRE_COUCH FECHA_COUCH '''
    if len(p) == 4:
        p[0] =  Tree('parametro', [p[1]], p[3])

def p_corpo(p):
    ''' corpo : corpo acao
                | vazio '''
    if len(p) == 2:
        p[0] = Tree('corpo', [p[1]], p[2])
    elif len(p) == 2:
        p[0] = Tree('corpo', [p[1]])

def p_acao(p):
    ''' acao : expressao
                | declaracao_variaveis
                | se
                | repita
                | leia
                | escreva
                | retorna
                | erro '''
    p[0] = Tree('acao', [p[1]])

def p_se(p):
    ''' se : SE expressao ENTAO corpo FIM
            | SE expressao ENTAO corpo SENAO corpo FIM '''
    if len(p) == 6:
        p[0] =  Tree('se', [p[2], p[4]])
    elif len(p) == 8:
        p[0] =  Tree('se', [p[2], p[4], p[6]])


def p_repita(p):
    ''' repita : REPITA corpo ATE expressao '''
    p[0] =  Tree('repita', [p[2], p[4]])

def p_atribuicao(p):
    ''' atribuicao : var ATRIBUICAO expressao '''
    p[0] =  Tree('atribuicao', [p[1], p[3]])

##Dar uma olhada
def p_leia(p):
    ''' leia : LEIA ABRE_PAREN var FECHA_PAREN '''
    p[0] = Tree('leia', [p[3]])

 def p_escreva(p):
        ''' escreva : ESCREVA ABRE_PAREN expressao FECHA_PAREN '''
        p[0] = Tree('escreva', [], p[3])

def p_retorna(p):
        ''' retorna : RETORNA ABRE_PAREN expressao FECHA_PAREN '''
        p[0] = Tree('retorna', [p[3]])

def p_expressao(p):
    ''' expressao : expressao_logica
                    | atribuicao '''
    p[0] = Tree('expressao', [p[1]])

## TEM Q MUDAR TUDO...
##VER
def p_expressao_logica(p):
    ''' expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples '''

def p_expressao_simples(p):
    ''' expressao_simples : expressao_aditiva
                            | expressao_simples operador_relacional expressao_aditiva '''
    if len(p) == 2:
        p[0] = Tree('expressao_simples', [p[1]])
    elif len(p) == 4:
        p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

def p_expressao_aditiva(p):
    ''' expressao_aditiva : expressao_multiplicativa
                            | expressao_aditiva operador_soma expressao_multiplicativa '''
    if len(p) == 2:
        p[0] = Tree('expressao_aditiva', [p[1]])
    elif len(p) == 4:
        p[0] = Tree('expressao_aditiva', [p[1], p[2], p[3]])