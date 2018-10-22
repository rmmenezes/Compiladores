# Autor: Caio Cesar Hideo Nakai
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz2.38/bin/'
from anytree import AnyNode, Node, RenderTree
from anytree.render import AsciiStyle, DoubleStyle
from anytree.exporter import DotExporter
from graphviz import Graph, Digraph


import sys
import ply.lex as lex
import ply.yacc as yacc
import logging

# listas que armazenam dados para tratamento de erro léxico
FECHA_CHAVES_SOLO = []
ABRE_CHAVES_LINHA = []
CARACTERES_INVALIDOS = []

# variavel sucesso analise sintática
ERRO_SINTATICO = False

# palavras reservadas da linguagem são definidas aqui
palavras_reservadas = {
	'se' : 'SE',
	'senão' : 'SENAO',
	'então' : 'ENTAO',
	'retorna' : 'RETORNA',
	'repita' : 'REPITA',
	'até' : 'ATE',
	'leia' : 'LEIA',
	'escreva' : 'ESCREVA',
	'fim' : 'FIM',
	'inteiro': 'TIPO_INTEIRO',
	'flutuante' : 'TIPO_FLUTUANTE',
}

# definição dos tokens utilizados
tokens = ['INTEIRO', 
		  'FLUTUANTE', 
		  'MAIS', 
		  'MENOS', 
		  'DIVIDIDO', 
		  'ATRIBUIR', 
		  'MULTIPLICA', 
		  'IDENTIFICADOR',
		  'FECHA_CHAVES_SOLO',
		  'ABRE_PARENTESES', 
		  'FECHA_PARENTESES',
		  'MAIOR', 
		  'MENOR', 
		  'MAIOR_IGUAL',
		  'MENOR_IGUAL', 
		  'DIFERENTE',
		  'DOIS_PONTOS',
		  'VIRGULA', 
		  'IGUAL', 
		  'ABRE_COLCHETES',
		  'FECHA_COLCHETES',
		  'NOVA_LINHA',
		  'E_LOGICO',
		  'OU_LOGICO',
		  ] + list(palavras_reservadas.values()) # concatenação com a lista de palavras reservadas!


# as variáveis precisam obrigatoriamente ter o mesmo nome dado na definição acima!
t_ignore =           ' \t'
t_MAIS =             r'\+'
t_MENOS =            r'\-'
t_MULTIPLICA =       r'\*'
t_DIVIDIDO = 	     r'/'
t_VIRGULA =          r','
t_ABRE_PARENTESES =  r'\('
t_FECHA_PARENTESES = r'\)'
t_ABRE_COLCHETES = 	 r'\['
t_FECHA_COLCHETES =  r'\]'
t_ATRIBUIR =         r'\:='
t_IGUAL =			 r'='
t_DOIS_PONTOS =      r':'
t_MAIOR_IGUAL =      r'\>='
t_MENOR_IGUAL =      r'\<='
t_MAIOR = 			 r'\>'
t_MENOR = 			 r'\<'
t_DIFERENTE =        r'<>'
# t_OU_LOGICO =        r'||'
t_E_LOGICO =         r'&&'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  INÍCIO DO TRATAMENTO DE COMENTÁRIO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

t_COMENTARIO_ignore = r'+ - * / , ( ) [ ] := >= <= > < =' 

# definição do estado de comentário
states = (
	("COMENTARIO", "inclusive"),
)

# quando ler "{" troca o estado para 'COMENTARIO'
def t_start_comentario(t):
	r'\{'
	# coloca a posicao da linha do abre chaves em uma lista 
	ABRE_CHAVES_LINHA.append(t.lineno)
	t.lexer.push_state('COMENTARIO')

# contador  de linhas enquanto está no estado comentario
def t_COMENTARIO_newline(t):
    r'\n'
    t.lexer.lineno += 1

# ignora tab
def t_COMENTARIO_tab(t):
    r'\t'


# ignora -> expressão regular para leitura de números ponto flutuante
def t_COMENTARIO_flut(t):
	r'\d+\.\d+ | \d+[eE][-+]\d+'

# ignora -> expressão regular para leitura de números naturais
def t_COMENTARIO_int(t):
	r'\d+'

# ignora -> textos
def t_COMENTARIO_ident(t):
	r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ_0-9]*'

# quando encontra '}' sai do estado 'COMENTARIO'
def t_COMENTARIO_end(t):
	r'\}'	
	if(ABRE_CHAVES_LINHA):
		ABRE_CHAVES_LINHA.pop()
	t.lexer.pop_state()

# se encontrar algum caractere diferente dos caracteres definidos acima, exibe a mensagem de erro
def t_COMENTARIO_error(t):
	# print("Caractere invalido no comentario'%s' linha %s" %(t.value[0], t.lineno))
	t.lexer.skip(1)

# conteúdo do comentário, ignora tudo q é diferente de '}' essa abordagem não conta linhas enquanto esta no
# estado COMENTARIO.
# def t_COMENTARIO_conteudo(t):
# 	r'[^}]+' 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  FIM DO TRATAMENTO DE COMENTÁRIO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXPRESSÕES REGULARES PARA LEITURA DOS TOKENS ~~~~~~~~~~~~~~~~~

# expressão regular para leitura de identificadores (nome de função/variável) 
def t_IDENTIFICADOR(t):
	r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ_0-9]*'
	t.type = palavras_reservadas.get(t.value, 'IDENTIFICADOR')
	return t

# conta '}' e coloca o numero da linha em uma lista
def t_FECHA_CHAVES_SOLO(t):
	r'\}'
	global FECHA_CHAVES_SOLO
	# FECHA_CHAVES += 1
	FECHA_CHAVES_SOLO.append(t.lineno)

# expressão regular para leitura de números ponto flutuante
def t_FLUTUANTE(t):
	r'\d+\. | \d+\d+ | \d+[eE][-+]\d+'
	t.value = float(t.value)
	return t

# expressão regular para leitura de números naturais
def t_INTEIRO(t):
	r'\d+'
	t.value = int(t.value)
	return t

# contador de linhas
def t_NOVA_LINHA(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


# se encontrar algum caractere inválido que não foi definido exibe mensagem de erro
def t_error(t):
	# print("Caractere invalido '%s' linha %s" %(t.value[0], t.lineno))
	CARACTERES_INVALIDOS.append((t.value[0], t.lineno))	
	t.lexer.skip(1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PARSER YACC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# classe arvore
class Tree:
	def __init__(self, type, children=None, leaf=None):
		self.type = type
		if children:
			self.children = children
		else:
			self.children = []	
		self.leaf = leaf



# define a precedência dos operadores aritméticos	
precedence = (
	('left', 'IGUAL', 'MAIOR', 'MENOR', 'MENOR_IGUAL', 'MAIOR_IGUAL'),
	('left', 'MAIS', 'MENOS'),
	('left', 'MULTIPLICA', 'DIVIDIDO')
)

def p_programa(p):
	'programa : lista_declaracoes'
	p[0] = Tree('programa', [p[1]])

def p_lista_declaracoes(p):
	'''lista_declaracoes : lista_declaracoes declaracao
						 | declaracao'''
	if len(p)==3:
		p[0] = Tree('lista_declaracoes', [p[1], p[2]])
	else:
		p[0] = Tree('lista_declaracoes', [p[1]])

def p_declaracao(p):
	'''declaracao : declaracao_variaveis
				  | inicializacao_variaveis
				  | declaracao_funcao'''
	p[0] = Tree('declaracao', [p[1]])

def p_declaracao_variaveis(p):
	'declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'
	p[0] = Tree('declaracao_variaveis', [p[1], p[3]])


def p_inicializacao_variaveis(p):
	'inicializacao_variaveis : atribuicao'
	p[0] = Tree('inicializacao_variaveis', [p[1]])

def p_lista_variaveis(p):
	'''lista_variaveis : lista_variaveis VIRGULA var
					   | var'''
	if len(p)==4:
		p[0] = Tree('lista_variaveis', [p[1],p[3]])
	else:
		p[0] = Tree('lista_variaveis', [p[1]])

def p_var(p):
	'''var : IDENTIFICADOR
		   | IDENTIFICADOR indice'''
	if len(p)==3:
		p[0] = Tree('var', [p[2]], p[1])
	else:
		p[0] = Tree('var', [], p[1])

def p_indice(p):
	'''indice : indice ABRE_COLCHETES expressao FECHA_COLCHETES
			  | ABRE_COLCHETES expressao FECHA_COLCHETES'''
	if len(p)==5:
		p[0] = Tree('indice', [p[1], p[3]])
	else:
		p[0] = Tree('indice', [p[2]])

def p_tipo(p):
	'''tipo : TIPO_INTEIRO
			| TIPO_FLUTUANTE'''
	p[0] = Tree('tipo', [], p[1])

def p_declaracao_funcao(p):
	'''declaracao_funcao : tipo cabecalho
						 | cabecalho'''
	if len(p)==3:
		p[0] = Tree('declaracao_funcao', [p[1],p[2]])
	else:
		p[0] = Tree('declaracao_funcao', [p[1]])

def p_cabecalho(p):
	'cabecalho : IDENTIFICADOR ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM'
	p[0] = Tree('cabecalho', [p[3], p[5]], p[1])

def p_lista_parametros(p):
	'''lista_parametros : lista_parametros VIRGULA parametro
						 | parametro
						 | vazio'''
	if len(p)==4:
		p[0] = Tree('lista_parametros', [p[1],p[3]])
	else:
		p[0] = Tree('lista_parametros', [p[1]])

def p_parametro(p):
	'''parametro : tipo DOIS_PONTOS IDENTIFICADOR
				 | parametro ABRE_COLCHETES FECHA_COLCHETES'''
	if p[2]=='DOIS_PONTOS':
		p[0] = Tree('parametro', [p[1]], p[3])
	else:
		p[0] = Tree('parametro', [p[1]])

def p_corpo(p):
	'''corpo : corpo acao
			 | vazio'''
	if len(p)==3:
		p[0] = Tree('corpo', [p[1],p[2]])
	else:
		p[0] = Tree('corpo', [p[1]])

def p_acao(p):
	'''acao : expressao
			| declaracao_variaveis
			| se
			| repita
			| leia
			| escreva
			| retorna'''
			# | erro'''
	p[0] = Tree('acao', [p[1]])

def p_se(p):
	'''se : SE expressao ENTAO corpo FIM
		  | SE expressao ENTAO corpo SENAO corpo FIM'''
	if len(p)==6:
		p[0] = Tree('se', [p[2],p[4]])
	else:
		p[0] = Tree('se', [p[2], p[4], p[6]])

def p_repita(p):
	'repita : REPITA corpo ATE expressao'
	p[0] = Tree('repita', [p[2], p[4]])

def p_atribuicao(p):
	'atribuicao : var ATRIBUIR expressao'
	p[0] = Tree('atribuicao', [p[1],p[3]])

def p_leia(p):
	'leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES'
	p[0] = Tree('leia', [p[3]])

def p_escreva(p):
	'''escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES'''
	p[0] = Tree('escreva', [p[3]])


def p_retorna(p):
	'retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES'
	p[0] = Tree('retorna', [p[3]])


def p_expressao(p):
	'''expressao : expressao_logica
				 | atribuicao'''
	p[0] = Tree('expressao', [p[1]]) 

def p_expressao_logica(p):
	'''expressao_logica : expressao_simples
						| expressao_logica operador_logico expressao_simples'''
	if len(p)==2:
		p[0] = Tree('expressao_logica', [p[1]])
	else:
		p[0] = Tree('expressao_logica', [p[1],p[2],p[3]])

def p_expressao_simples(p):
	'''expressao_simples : expressao_aditiva
						 | expressao_simples operador_relacional expressao_aditiva'''
	if len(p)==2:
		p[0] = Tree('expressao_simples', [p[1]])
	else:
		p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

def p_expressao_aditiva(p):
	'''expressao_aditiva : expressao_multiplicativa
						 | expressao_aditiva operador_soma expressao_multiplicativa'''
	if len(p)==2:
		p[0] = Tree('expressao_aditiva', [p[1]])
	else:
		p[0] = Tree('expressao_aditiva', [p[1],p[2],p[3]])

def p_expressao_multiplicativa(p):
	'''expressao_multiplicativa : expressao_unaria
								| expressao_multiplicativa operador_multiplicacao expressao_unaria'''
	if len(p)==2:
		p[0] = Tree('expressao_multiplicativa', [p[1]])
	else:
		p[0] = Tree('expressao_multiplicativa', [p[1],p[2],p[3]])

def p_expressao_unaria(p):
	'''expressao_unaria : fator
						| operador_soma fator'''
						# | operador_negacao fator'''
	if len(p)==2:
		p[0] = Tree('expressao_unaria', [p[1]])
	else:
		p[0] = Tree('expressao_unaria', [p[1],p[2]])


def p_operador_relacinal(p):
	'''operador_relacional : MENOR
						   | MAIOR
						   | IGUAL
						   | DIFERENTE
						   | MENOR_IGUAL
						   | MAIOR_IGUAL'''
	p[0] = Tree('operador_relacional', [], p[1])

def p_operador_soma(p):
	'''operador_soma : MAIS
					 | MENOS'''
	p[0] = Tree('operador_soma', [], p[1])

def p_operador_logico(p):
	'''operador_logico : E_LOGICO
					   | OU_LOGICO'''
	p[0] = Tree('operador_logico', [], p[1])

def p_operador_multiplicacao(p):
	'''operador_multiplicacao : MULTIPLICA
							  | DIVIDIDO'''
	p[0] = Tree('operador_multiplicacao', [], p[1])

def p_fator(p):
	'''fator : ABRE_PARENTESES expressao FECHA_PARENTESES
			 | var
			 | chamada_funcao
			 | numero'''
	if len(p)==2:
		p[0] = Tree('fator', [p[1]])
	else:
		p[0] = Tree('fator', [p[2]])

def p_numero(p):
	'''numero : INTEIRO
			  | FLUTUANTE'''
	p[0] = Tree('numero', [], p[1])

def p_chamada_funcao(p):
	'chamada_funcao : IDENTIFICADOR ABRE_PARENTESES lista_argumentos FECHA_PARENTESES'
	p[0] = Tree('chamada_funcao', [p[3]], p[1])

def p_lista_argumentos(p):
	'''lista_argumentos : lista_argumentos VIRGULA expressao
						| expressao
						| vazio'''
	if len(p)==2:
		p[0] = Tree('lista_argumentos', [p[1]])
	else:
		p[0] = Tree('lista_argumentos', [p[1],p[3]])

def p_vazio(p):
	'vazio : '
	p[0] = Tree("vazio")
	pass

# ~~~~~~~~~~ alguns tratamentos de erro simples ~~~~~~~~~~~~~~~~~~~

def p_error(p):
	global ERRO_SINTATICO
	ERRO_SINTATICO = True
	if p:
		print('Erro sintatico: %s na linha %d' % (p.value, p.lineno))

	else:
		print('Esta faltando um "fim"')

def p_retorna_error(p): ok
	'retorna : RETORNA ABRE_PARENTESES error FECHA_PARENTESES'
	print("Função retorna não está recebendo nenhum argumento")

def p_declaracao_variaveis_error(p): ok
	'declaracao_variaveis : error DOIS_PONTOS lista_variaveis'
	print("Dica: possível erro na declaração de variável")

def p_indice_error(p): ok
	'''indice : indice ABRE_COLCHETES error FECHA_COLCHETES
		  | ABRE_COLCHETES error FECHA_COLCHETES'''
	print("Dica: possível erro no índice entre colchetes")

def p_declaracao_cabecalho_error(p):
	'cabecalho : IDENTIFICADOR ABRE_PARENTESES lista_parametros FECHA_PARENTESES error FIM'
	print("Dica: possível erro no cabeçalho da função")

def p_atribuicao_error(p): ok
	'atribuicao : error ATRIBUIR expressao'
	print("Dica: possível erro na atribuição")

def p_leia_error(p): ok
	'leia : LEIA ABRE_PARENTESES error FECHA_PARENTESES'
	print("Função leia não está recebendo nenhum argumento")

def p_escreva_error(p): ok
	'''escreva : ESCREVA ABRE_PARENTESES error FECHA_PARENTESES'''
	print("Função escreva não está recebendo nenhum argumento")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FIM PARSER YACC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

count = 0
# função recursiva para percorrer a árvore gerada e colocar no padrão aceito pela biblioteca anytree
def inorderTraversal2(root, pai= None):
	if root:
		temp = Node(root.type, parent= pai)
		if(root.leaf):
			Node(root.leaf, parent=temp)

		for filho in root.children:
			inorderTraversal2(filho,temp)

		return temp

def inorderTraversal3(root, pai= None):
	global dot, count
	if root:
		count += 1
		id = str(root.type)+str(count)

		dot.node(id, str(root.type))
		if pai:
			dot.edge(pai,id)
		if(root.leaf):
			count+=1
			id_leaf = str(root.leaf)+str(count)
			dot.node(id_leaf, str(root.leaf))
			dot.edge(id,id_leaf)

		for filho in root.children:
			inorderTraversal3(filho,id)

		return 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  メインコード ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# abre o arquivo e armazena o contéudo na variável data
f = open(sys.argv[1], "r",  encoding="utf-8")
data = f.read()

# analisador léxico
lex.lex()
lex.input(data)
# log = logging.getLogger('ply')

# analisador sintático
parser = yacc.yacc(debug=True)
g = Graph(format='png')
dot = Digraph(comment='The Round Table')
# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')
# dot.edge('B', 'L')
result = parser.parse(data)
inorderTraversal3(result)
dot.render('test-output/round-table.gv', view=True) 
# código para printar arvore sintática, caso seja digitado o comando Tree
if(not ERRO_SINTATICO):
	print("Análise sintática realizada com sucesso")
	if len(sys.argv) > 2:
		if sys.argv[2]=="-t":
			a = inorderTraversal2(result)
			DotExporter(a).to_dotfile("arvore.dot") #picture gera img
			for pre, _, node in RenderTree(a,style=DoubleStyle()):
				print("%s%s" % (pre, node.name))
			

# exibição dos erros gerados pelo analisador léxico
lista = []
while True:
	tok = lex.token()
	if not tok: break
	lista.append((tok.type,str(tok.value)))
	# parser.parse(tok)
if FECHA_CHAVES_SOLO or ABRE_CHAVES_LINHA:
	while FECHA_CHAVES_SOLO:
		print('Foi fechado \'}\', mas nao foi aberto! Linha:', FECHA_CHAVES_SOLO.pop())
	while ABRE_CHAVES_LINHA:
		print('Foi aberto \'{\', mas nao foi fechado! Linha:', ABRE_CHAVES_LINHA.pop())

elif CARACTERES_INVALIDOS:
	for i in range(len(CARACTERES_INVALIDOS)):
		print("Caractere Invalido: '%s', Linha: %s" % CARACTERES_INVALIDOS[i])

# exibe a lista de tokens gerada pelo analisador léxico, necessário comentar o yacc para ver a lista
else:
	for i in range(len(lista)):
		print(lista[i])

