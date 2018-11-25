### Rafael Menzes Barboza, RA: 1817485 ###
from graphviz import Digraph
import sys
from datetime import datetime
from syn import *
from poda import *
global pilhaEscopos
pilhaEscopos = ['global']


class Verifica_Arvore():
    def andar(self, raiz, TabSimb):
        if raiz:
            for filho in raiz.child:
                if filho.type == "declaracao_variaveis":
                    self.declaracao_variaveis(filho, TabSimb)
                elif filho.type == "declaracao_funcao":
                    self.declaracao_funcao(filho, TabSimb)
                elif filho.type == "retorna":
                    self.retorna(filho, TabSimb)
                elif filho.type == "atribuicao":
                    self.atribuicao(filho, TabSimb)
                # elif filho.type == "chamada_funcao":
                # elif filho.type == "fim":
                # elif filho.type == "até":
                if not isinstance(filho, Tree):
                    return
                self.andar(filho, TabSimb)
        else:
            return

    def get_value_no_folhas_para_variaveis(self, filho):
        lista_values = []
        index_valor = None
        index_tipo = None
        for i in filho.child:
            if i.value != 'vazio' and len(i.child) == 0:
                lista_values.append(i.value)
            elif i.value != 'vazio' and len(i.child) == 1:
                lista_values.append(i.value)
                index_tipo = i.child[0].child[0].type
                index_valor = i.child[0].child[0].value
        return lista_values, index_valor, index_tipo

    def get_value_no_folhas(self, filho):
        lista_values = []
        for i in filho.child:
            if i.value != 'vazio':
                lista_values.append(i.value)
        return lista_values

    def atribuicao(self, filho, TabSimb):
        variavel = filho.child[0].value
        find_e = TabSimb.find_elemento(variavel)
        if find_e == None:
            print("Erro: A variavel '" + variavel + "' que deseja atribuir, ainda não foi declarada")
        else:
            expressao = self.resolve_expressao(filho.child[1], TabSimb)
            tipo = expressao[0]
            valor = expressao[1]
            find_e.valor = valor
            find_e.used = True

        
    
    def retorna_o_tipo_do_no_passado(self, no, TabSimb):
        if (str(type(no.value)) == "<class 'str'>"):
            elemento = TabSimb.find_elemento(no.value)
            return elemento.tipo
        else:
            try:
                int(no.value)
                return "inteiro"
            except ValueError:
                float(no.value)
                return "flutuante"

    def devolve_valor_final_expressao(self, filho_esquerda, operador, filho_direita, TabSimb):
        num_esquerdo = filho_esquerda.value
        num_direito = filho_direita.value
        if str(filho_direita) == "var":
            find_e = TabSimb.find_elemento(filho_direita.value)
            if find_e == None:
                print("Erro: A variavel '" + filho_direita.value + "' ainda nao foi declarada")
            elif find_e != None:
                if find_e.valor == "null":
                    print("Erro: A variavel '" + filho_direita.value + "' não possui nenhum valor atribuido")
                    exit(1)
                else:
                    find_e.used = True
                    num_direito = find_e.valor

        if str(filho_esquerda) == "var":
            find_e = TabSimb.find_elemento(filho_esquerda.value)
            if find_e == None:
                print("Erro: A variavel '" + filho_esquerda.value + "' ainda nao foi declarada")
            elif find_e != None:
                if find_e.valor == "null":
                    print("Erro: A variavel '" + filho_esquerda.value + "' não possui nenhum valor atribuido")
                    exit(1)
                else:
                    find_e.used = True
                    num_esquerdo = find_e.valor
        
        if operador.type == "operador_soma":
            if operador.value == "+":
                return num_esquerdo + num_direito
            else:
                return num_esquerdo - num_direito
        elif operador.type == "operador_multiplicacao":
            if operador.value == "*":
                return num_esquerdo * num_direito            
            else:
                return num_esquerdo / num_direito
        else:
            return "expressao ainda nao foi declarada"

    def resolve_expressao(self, filho, TabSimb):
        if len(filho.child) == 1:
            tipo_meio = self.retorna_o_tipo_do_no_passado(filho.child[0], TabSimb)
            result = filho.child[0].value
            return tipo_meio, result
        if len(filho.child) > 1:
            filho_esquerda = filho.child[0]
            operador = filho.child[1]
            filho_direita = filho.child[2]
            tipo_direita = self.retorna_o_tipo_do_no_passado(filho_direita, TabSimb) 
            tipo_esquerda = self.retorna_o_tipo_do_no_passado(filho_esquerda, TabSimb)
            if tipo_direita != tipo_esquerda:
                print("Aviso: A expressão trabalha com tipos diferentes " + tipo_direita + " e " + tipo_esquerda)
                result = self.devolve_valor_final_expressao(filho_esquerda, operador, filho_direita, TabSimb)
                print(result)
                return tipo_direita, result
            else:
                result = self.devolve_valor_final_expressao(filho_esquerda, operador, filho_direita, TabSimb)
                print(result)
                return tipo_direita, result

                

    def retorna(self, filho, TabSimb):
        funcao = TabSimb.find_funcao(pilhaEscopos[-1])
        if funcao != None:
            if funcao.tipo_retorno == self.resolve_expressao(filho.child[0], TabSimb):
                pilhaEscopos.pop()
            else:
                print("Erro: A função esta retornando um tipo diferente do delcarado")
        else:
            print("Erro: O progama esta retornado algo fora de um escopo valido")

    def declaracao_funcao(self, filho, TabSimb):
        lista_paramentros = self.get_value_no_folhas(filho.child[1].child[0])
        tipo = filho.child[0].value
        nome = filho.child[1].value
        self.declara_funcao_na_tabela_de_simbolos(nome, lista_paramentros, tipo, TabSimb)
        if nome == "principal":
            TabSimb.TemPrincipal = True

    def declara_funcao_na_tabela_de_simbolos(self, nome, lista_paramentros, tipo, TabSimb):
        if TabSimb.find_funcao(nome) != None:
            print("Aviso: Função '" + nome + "' já declarada anteriormente")
        else:
            TabSimb.inserir_funcao(nome, tipo, 'null', False, lista_paramentros)

    def declara_variaveis_na_tabela_de_simbolos(self, lista_variaveis, tipo, index, TabSimb):
        for variavel in lista_variaveis:
            if(TabSimb.find_elemento(variavel) != None):
                print("Aviso: Variável '" + variavel + "' já declarada anteriormente")
            else:
                TabSimb.inserir_elemento(variavel, tipo, "null", index, False)

    def declaracao_variaveis(self, filho, TabSimb):
        resultado = self.get_value_no_folhas_para_variaveis(filho.child[1])
        lista_variaveis = resultado[0]
        index_valor = resultado[1]
        index_tipo = resultado[2]
        tipo = filho.child[0].value
        if index_tipo != "numero_int" and index_valor != None:
            print("Erro: índice de array '" + str(index_valor) + "' não inteiro")
        else:
            self.declara_variaveis_na_tabela_de_simbolos(lista_variaveis, tipo, index_valor, TabSimb)


class ListaFuncoes():
    def __init__(self, nome, tipo_retorno, valor_retorno, lista_paramentros, foi_retornada, escopo):
        self.nome = nome
        self.tipo_retorno = tipo_retorno
        self.valor_retorno = valor_retorno
        self.lista_paramentros = lista_paramentros
        self.escopo = escopo
        self.foi_retornada = foi_retornada
        pilhaEscopos.append(nome)


class TabelaSimbolos():
    TemPrincipal = False

    def __init__(self):
        self.lista_elementos = []
        self.lista_funcoes = []

    def pega_lista_funcoes(self):
        return self.lista_funcoes

    def inserir_elemento(self, nome, tipo, valor, indice, used):
        self.lista_elementos.append(Elemento(nome, pilhaEscopos[-1], tipo, valor, indice, used))

    def inserir_funcao(self, nome, tipo_retorno, valor_retorno, foi_retornada, lista_paramentros):
        self.lista_funcoes.append(ListaFuncoes(nome, tipo_retorno, valor_retorno, lista_paramentros, foi_retornada, pilhaEscopos[-1]))

    def print_pilha(self):
        print("### PILHA DE ESCOPOS ###")
        for elemento in pilhaEscopos:
            print(elemento)

    def print_tabela_simbolos(self):
        print("### TABELA DE SIMBOLOS ###")
        for e in self.lista_elementos:
            if(e.indice):
                print("Tipo: " + e.tipo + " Nome: " + e.nome + " Indice: " + e.indice +
                      " Valor: " + str(e.valor) + " Escopo: " + e.escopo + " Usada: " + str(e.used))
            else:
                print("Tipo: " + e.tipo + " Nome: " + e.nome + " Valor: " +
                      str(e.valor) + " Escopo: " + e.escopo + " Usada: " + str(e.used))

    def find_elemento(self, var):
        for escopo in pilhaEscopos:
            for elemento in self.lista_elementos:
                if elemento.nome == var and elemento.escopo == escopo:
                    return elemento
        return None
    
    def find_funcao(self, nome):
        for funcao in self.lista_funcoes:
            if funcao.nome == nome:
                return funcao
        return None

    def print_tabela_funcoes(self):
        print("### TABELA DE FUNCOES ###")
        for f in self.lista_funcoes:
            print("Nome: " + f.nome + " Lista_Parametros: " + str(f.lista_paramentros) + " Tipo_Retorno: " +
                  str(f.tipo_retorno) + " Valor_Retorno: " + str(f.valor_retorno) + " Escopo: " + str(f.escopo))

    def conferir_variaveis_usadas(self):
        if self.lista_elementos:
            for elemento in self.lista_elementos:
                if elemento.used == False:
                    print ("Aviso: Variável '" + elemento.nome +"' declarada e não utilizada")

    #def conferir_funcoes_declaradas(self):
    #    if self.lista_funcoes:
    #        for f in self.lista_funcoes:
    #            if(f.foi_retornada == False):
    #                print("Erro: Função " + f.nome + " deveria retornar " + f.tipo_retorno + ", mas retorna vazio")

class Elemento():
    def __init__(self, nome, escopo, tipo, valor, indice, used):
        self.nome = nome
        self.escopo = escopo
        self.tipo = tipo
        self.valor = valor
        self.used = used
        self.indice = indice

    def set_uso(self, elemento, usado):
        if(elemento):
            elemento.used = usado
        else:
            print("Erro: Variavel ainda nao declarada")
            exit(1)

    def set_valor(self, elemento, valor, TabSimb):
        elemento.valor = valor

    def get_tipo(self, elemento):
        return elemento.tipo

    def set_tipo(self, elemento, tipo):
        elemento.tipo = tipo


if __name__ == '__main__':
    now = datetime.now()
    root = Syn()                        # Chama o analisador Sintatico
    TrimTree(root.ps)                   # Poda a arvore
    dot = Digraph(comment='TREE')       # Abaixo é o processo de impressão
    Sintatico = Verifica_Arvore()
    TabSimb = TabelaSimbolos()
    Sintatico.andar(root.ps, TabSimb)

    
    if(TabSimb.TemPrincipal == False):      #VERIFICA SE TEM A FUNÇÃO PRINCIPAL
        print ("Erro: Função principal não declarada")

    TabSimb.conferir_variaveis_usadas()     
    #TabSimb.conferir_funcoes_declaradas()

    TabSimb.print_tabela_simbolos()
    #TabSimb.print_tabela_funcoes()
    #TabSimb.print_pilha()

    

    print_tree(root.ps, dot)
    # print(dot.source)
    dot.render('PrintArvore/Saida'+str(sys.argv[1])+str(now.day)+'-'+str(now.month)+'-' + str(
        now.year)+'h' + str(now.hour)+'m'+str(now.minute)+'s'+str(now.second)+'.gv.pdf', view=True)
