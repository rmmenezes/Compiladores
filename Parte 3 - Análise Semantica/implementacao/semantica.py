### Rafael Menzes Barboza, RA: 1817485 ###
from graphviz import Digraph
import sys
from datetime import datetime
from syn import *
from poda import *
global pilhaEscopos
pilhaEscopos = ["global"]


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
                elif filho.type == "chamada_funcao":
                    self.chamada_funcao(filho, TabSimb)
                elif filho.type == "escreva":
                    self.escreva(filho, TabSimb)
                elif filho.type == "leia":
                    self.leia(filho, TabSimb)
                elif filho.type == "se":
                    self.se(filho, TabSimb)
                elif filho.type == "repita":
                    self.repita(filho, TabSimb)
                elif filho.type == "até":
                    self.ate(filho, TabSimb)
                elif filho.type == "fim":
                    self.fim(filho, TabSimb)
                
                
                # elif filho.type == "até":
                if not isinstance(filho, Tree):
                    return
                self.andar(filho, TabSimb)
        else:
            return

    def get_no_folhas_para_variaveis(self, filho):
        lista_values = []
        index_valor = None
        index_tipo = None
        for i in filho.child:
            if i.value != 'vazio' and len(i.child) == 0:
                lista_values.append(i)
            elif i.value != 'vazio' and len(i.child) == 1:
                lista_values.append(i)
                index_tipo = i.child[0].child[0].type
                index_valor = i.child[0].child[0].value
        return lista_values, index_valor, index_tipo

    def get_value_no_folhas(self, filho):
        lista_values = []
        for i in filho.child:
            if i.value != 'vazio':
                lista_values.append(i.value)
        return lista_values

    def fim(self, filho, TabSimb):
        pilhaEscopos.pop()
    
    def ate(self, filho, TabSimb):
        pilhaEscopos.pop()

    def repita(self, filho, TabSimb):
        TabSimb.inserir_funcao(filho.type, None, None, None, None)
        expressao = filho.child[1]
        self.resolve_expressao(expressao, TabSimb, filho.type)


    def se(self, filho, TabSimb):
        TabSimb.inserir_funcao(filho.type, None, None, None, None)

    def escreva(self, filho, TabSimb):
        if filho.child[0] == "chamada_funcao":
            funcao = TabSimb.find_funcao(filho.child[0].value)
            if funcao!=None:
                funcao.used = True
            else:
                print("Linha:["+str(filho.linha)+"] Erro: Chamada da função '" + filho.child[0].value + "' que não foi declarada")
        elif filho.child[0] == "var":
            variavel = filho.child[0].value
            find_e = TabSimb.find_elemento(variavel)
            if find_e!=None:
                find_e.used = True
            else:
                print("Linha:["+str(filho.linha)+"] Erro: A variavel '"+ filho.child[0].value +"' não está declarada")
        else:
            print("Linha:["+str(filho.linha)+"] Erro: Não foi possivel realizar a escrita")
    
    def leia(self, filho, TabSimb):
        if filho.child[0] == "chamada_funcao":
            funcao = TabSimb.find_funcao(filho.child[0].value)
            if funcao!=None:
                funcao.used = True
            else:
                print("Linha:["+str(filho.linha)+"] Erro: Chamada da função '" + filho.child[0].value + "' que não foi declarada")
        elif filho.child[0] == "var":
            variavel = filho.child[0].value
            find_e = TabSimb.find_elemento(variavel)
            if find_e!=None:
                find_e.used = True
            else:
                print("Linha:["+str(filho.linha)+"] Erro: A variavel '"+ filho.child[0].value +"' não está declarada")
        else:
            print("Linha:["+str(filho.linha)+"] Erro: Não foi possivel realizar a escrita")

    def chamada_funcao(self, filho, TabSimb):
        nome = filho.value
        if nome == "principal":
            print("Erro: Chamada para a função principal não permitida")
            exit(1)
        lista_arg = []
        for arg in filho.child[0].child:
            no_folha = self.get_value_no_folhas(arg)
            if len(no_folha) > 0:
                lista_arg.append(no_folha)
        funcao = TabSimb.find_funcao(nome)
        if(funcao != None):
            if (len(funcao.lista_paramentros) > len(lista_arg)):
                print("Erro: Chamada à função '" + nome + "' com número de parâmetros menor que o declarado")
            elif (len(funcao.lista_paramentros) < len(lista_arg)):
                print("Erro: Chamada à função '" + nome + "' com número de parâmetros maior que o declarado")
            else:
                funcao.used = True
        else:
            print("Erro: Chamada da função '" + nome + "' que não foi declarada")

    def atribuicao(self, filho, TabSimb):
        variavel = filho.child[0]
        index = None
        if len(variavel.child) > 0:
            index = variavel.child[0].child[0]
        find_e = TabSimb.find_elemento(variavel.value)
        if find_e == None:
            print("Linha:["+str(variavel.linha)+"] Erro: A variavel '" + variavel.value + "' que deseja atribuir, ainda não foi declarada")
        else:
            find_e.used = True
            if index != None:
                if index.type == "var":
                    e = TabSimb.find_elemento(index.value)
                    if e:
                        e.used = True
                        index = e.valor
                        if int(float(index)) != None and find_e.indice < int(float(index)):
                            print("Erro: O vetor '" + variavel.value + "' que deseja atribuir, esta fora do range declarado")
                    else:
                        print("BLA")
                else:
                    expressao = self.resolve_expressao(filho.child[1], TabSimb, pilhaEscopos[-1])
                    tipo = expressao[0]
                    valor = expressao[1]
                    index = int(float(index))
                    if index < find_e.indice:
                        find_e.used = True
                        if tipo == find_e.tipo:
                            find_e.valor[index] = valor
                        else:
                            print("Linha:["+str(filho.linha)+"] Aviso: A variavel '" + find_e.nome + "' tem tipo '" + find_e.tipo + "' mas esta recebendo um valor '" + str(valor) + "' de tipo '"+ tipo +"' hove a alterção deste tipo para o tipo da variavel a ser atribuida")
                            novo_valor = self.muda_o_tipo(find_e.tipo, valor)
                            find_e.valor = novo_valor
            else:
                if filho.child[1].child[0].type == "chamada_funcao":
                    find_f = TabSimb.find_funcao(filho.child[1].child[0].value)
                    print("find_f.nome")
                    tipo = find_f.tipo_retorno
                    find_e.used = True
                    if tipo == find_e.tipo:
                        find_e.valor = valor
                    else:
                        print("Linha:["+str(filho.linha)+"] Aviso: A variavel '" + find_e.nome + "' tem tipo '" + find_e.tipo + "' mas esta recebendo um valor '"+ str(valor) + "' de tipo '"+ tipo +"' hove a alterção deste tipo para o tipo da variavel a ser atribuida")
                        novo_valor = self.muda_o_tipo(find_e.tipo, valor)
                        find_e.valor = novo_valor
                else:
                    expressao = self.resolve_expressao(filho.child[1], TabSimb, pilhaEscopos[-1])
                    tipo = expressao[0]
                    valor = expressao[1]
                    find_e.used = True
                    if tipo == find_e.tipo:
                        find_e.valor = valor
                    else:
                        print("Linha:["+str(filho.linha)+"] Aviso: A variavel '" + find_e.nome + "' tem tipo '" + find_e.tipo + "' mas esta recebendo um valor '" + str(valor) + "' de tipo '"+ tipo +"' hove a alterção deste tipo para o tipo da variavel a ser atribuida")
                        novo_valor = self.muda_o_tipo(find_e.tipo, valor)
                        find_e.valor = novo_valor

    def str_or_int(self, s):
        try:
            int(s)
            return "inteiro"
        except ValueError:
            return "varivael"


    def retorna_o_tipo_do_no_passado(self, no, TabSimb):
        if str(type(no.value)) == "<class 'str'>":
            if self.str_or_int(no.value) == "inteiro":
                return "inteiro"
            else:
                elemento = TabSimb.find_elemento(no.value)
                if elemento != None:
                    return elemento.tipo
                else:
                    print("Erro: A variavel '"+ no.value +"' não está declarada")
                    exit(1)
        elif str(type(no.value)) == "<class 'float'>":
            return "flutuante"
        elif str(type(no.value)) == "<class 'int'>":
            return "inteiro"

    def devolve_valor_final_expressao(self, filho_esquerda, operador, filho_direita, TabSimb):
        num_direito = filho_direita.value
        num_esquerdo = filho_esquerda.value
        if str(filho_direita) == "var" and filho_direita != None:
            find_e = TabSimb.find_elemento(filho_direita.value)
            if find_e == None:
                print("Linha:["+str(filho_direita.linha)+"] Erro: A variavel '" + filho_direita.value + "' ainda não foi declarada")
            elif find_e != None:
                if find_e.valor == "null" and find_e.ehParametro == False:
                    print("Erro: A variavel '" + filho_direita.value + "' não possui nenhum valor atribuido")
                    exit(1)
                elif find_e.valor == "null" and find_e.ehParametro == True:
                    find_e.used = True
                else:
                    find_e.used = True
                    num_direito = find_e.valor

        if str(filho_esquerda) == "var" and filho_esquerda != None:
            find_e = TabSimb.find_elemento(filho_esquerda.value)
            if find_e == None:
                print("Linha:["+str(filho_esquerda.linha)+"] Erro: A variavel '" + filho_esquerda.value + "' ainda não foi declarada")
            elif find_e != None:
                if find_e.valor == "null" and find_e.ehParametro == False:
                    print("Erro: A variavel '" + filho_esquerda.value + "' não possui nenhum valor atribuido")
                    exit(1)
                elif find_e.valor == "null" and find_e.ehParametro == True:
                    find_e.used = True
                else:
                    find_e.used = True
                    num_esquerdo = find_e.valor

        if operador.type == "operador_soma":
            if operador.value == "+":
                if str(type(num_esquerdo)) == "<class 'str'>" or str(type(num_direito)) == "<class 'str'>":
                    return (str(num_direito) + " + " + str(num_esquerdo))
                else: 
                    return num_esquerdo + num_direito
            else:
                if str(type(num_esquerdo)) == "<class 'str'>" or str(type(num_direito)) == "<class 'str'>":
                    return (str(num_direito) + " - " + str(num_esquerdo))
                else:
                    return num_esquerdo - num_direito
        elif operador.type == "operador_multiplicacao":
            if operador.value == "*":
                if str(type(num_esquerdo)) == "<class 'str'>" or str(type(num_direito)) == "<class 'str'>":
                    return (str(num_direito) + " * " + str(num_esquerdo))
                else:
                    return num_esquerdo * num_direito
            else:
                if str(type(num_esquerdo)) == "<class 'str'>" or str(type(num_direito)) == "<class 'str'>":
                    return (str(num_direito) + " / " + str(num_esquerdo))
                else:
                    return num_esquerdo / num_direito

        elif operador.type == "operador_relacional":
            if operador.value == ">":
                if str(type(num_esquerdo)) == "<class 'str'>" or str(type(num_direito)) == "<class 'str'>":
                    return (str(num_direito) + " > " + str(num_esquerdo))
                else:
                    return num_esquerdo > num_direito
            else:
                if str(type(num_esquerdo)) == "<class 'str'>" or str(type(num_direito)) == "<class 'str'>":
                    return (str(num_direito) + " < " + str(num_esquerdo))
                else:
                    return num_esquerdo < num_direito

    def muda_o_tipo(self, tipo_cetro, valor):
        if tipo_cetro == "inteiro" and str(type(valor)) != "<class 'str'>":
            return int(float(valor))
        elif tipo_cetro == "flutuante" and str(type(valor)) != "<class 'str'>":
            return float(int(valor))
        else:
            return valor
        

    def resolve_expressao(self, filho, TabSimb, funcao):
        if len(filho.child) == 1:
            funcao_escopo = TabSimb.find_funcao(funcao)
            result = filho.child[0].value
            if filho.child[0].type == "var":
                variavel = TabSimb.find_elemento(filho.child[0].value)
                if variavel != None and (variavel.valor != "null" or variavel.ehParametro ==True):
                    tipo_meio = self.retorna_o_tipo_do_no_passado(filho.child[0], TabSimb)
                    return tipo_meio, variavel.valor
                else:
                    print("Linha:["+str(filho.child[0].linha)+"] Erro: A variavel '" + filho.child[0].value + "' ainda não foi declarada")
                    exit(1)
            else:
                tipo_meio = self.retorna_o_tipo_do_no_passado(filho.child[0], TabSimb)
                return tipo_meio, result
        if len(filho.child) == 3:
            funcao_escopo = TabSimb.find_funcao(funcao)
            filho_esquerda = filho.child[0]
            operador = filho.child[1]
            filho_direita = filho.child[2]
            tipo_direita = self.retorna_o_tipo_do_no_passado(filho_direita, TabSimb)
            tipo_esquerda = self.retorna_o_tipo_do_no_passado(filho_esquerda, TabSimb)
            if tipo_direita != tipo_esquerda:
                print("Linha:["+str(operador.linha)+"] Aviso: A expressão trabalha com tipos diferentes " + tipo_direita + " e " + tipo_esquerda + " houve uma coerção implícita") 
                novo_result = self.devolve_valor_final_expressao(filho_esquerda, operador, filho_direita, TabSimb)
                return tipo_direita, novo_result
            else:
                result = self.devolve_valor_final_expressao(filho_esquerda, operador, filho_direita, TabSimb)
                if tipo_esquerda != funcao_escopo.tipo_retorno and funcao_escopo.tipo_retorno != None:
                    print ("Linha:["+str(operador.linha)+"] Aviso: A funcão '" + str(funcao_escopo.nome) + "' deveria retornar '" + str(funcao_escopo.tipo_retorno) + "' mas retorna '" + str(tipo_esquerda) + "' houve uma coerção implícita")
                    novo_result = self.muda_o_tipo(funcao_escopo.tipo_retorno, result)
                    return funcao_escopo.tipo_retorno, novo_result
                else:
                    return tipo_direita, result 



    def retorna(self, filho, TabSimb):
        funcao = TabSimb.find_funcao(pilhaEscopos[-1])
        if funcao.escopo_pai != "global":               #SE NAO FOR UMA FUNCAO COMUM 
            while funcao.escopo_pai != "global":
                funcao = TabSimb.find_funcao(funcao.escopo_pai)   #SE FOR UMA FUNCAO COMUM

        if funcao != None:
            expressao = self.resolve_expressao(filho.child[0], TabSimb, funcao.nome)
            tipo = expressao[0]
            resultado = expressao[1]

            if str(tipo) != str(funcao.tipo_retorno):
                if(funcao.tipo_retorno == "vazio"):
                    print("Linha:["+str(filho.linha)+"] Erro: Função '"+str(funcao.nome)+"' do tipo vazio retornando '"+ str(tipo) +"'")
                else:
                    print ("Linha:["+str(filho.linha)+"] Erro: A funcão '" + str(funcao.nome) + "' deveria retornar '" + str(funcao.tipo_retorno) + "' mas retorna '" + str(tipo) + "'")
            elif funcao.tipo_retorno == tipo:
                funcao.foi_retornada = True
            else:
                print("Erro: A função esta retornando um tipo diferente do delcarado")
        else:
            print("Erro: O progama esta retornado algo fora de um escopo valido")


    def declaracao_funcao(self, filho, TabSimb):
        if filho.child[0].type == "tipo":
            tipo = filho.child[0].value
            nome = filho.child[1].value
            lista_paramentros = []
            self.declara_funcao_na_tabela_de_simbolos(nome, lista_paramentros, tipo, TabSimb, filho)
            for param in filho.child[1].child[0].child:
                for tipo in param.child:
                    ehParametro = True
                    TabSimb.inserir_elemento(param.value, tipo.value, "null", None, True, nome, ehParametro)
                    lista_paramentros.append(param.value)
            if nome == "principal":
                TabSimb.TemPrincipal = True
        else:
            tipo = "vazio"
            nome = filho.child[0].value
            lista_paramentros = []
            self.declara_funcao_na_tabela_de_simbolos(nome, lista_paramentros, tipo, TabSimb, filho)
            for param in filho.child[0].child[0].child:
                for tipo in param.child:
                    ehParametro = True
                    TabSimb.inserir_elemento(param.value, tipo.value, "null", None, True, nome, ehParametro)
                    lista_paramentros.append(param.value)
            if nome == "principal":
                TabSimb.TemPrincipal = True

    def declara_funcao_na_tabela_de_simbolos(self, nome, lista_paramentros, tipo, TabSimb, no):
        if TabSimb.find_funcao(nome) != None:
            print("Linha:["+no.linha+"] Aviso: Função '" + nome + "' já declarada anteriormente")
        else:    
            TabSimb.inserir_funcao(nome, str(tipo), False, lista_paramentros, False, no.linha)
            

    def declara_variaveis_na_tabela_de_simbolos(self, lista_variaveis, tipo, index, TabSimb):
        for variavel in lista_variaveis:
            if(TabSimb.find_elemento(variavel.value) != None):
                print("Linha:["+str(variavel.linha)+"] Aviso: Variável '" + variavel.value + "' já declarada anteriormente")
            elif index != None:
                index = int(float(index))
                v = []
                for i in range(int(float(index))):
                    v.append('null')
                TabSimb.inserir_elemento(variavel.value, tipo, v, index, False, pilhaEscopos[-1], False, variavel.linha)
            else:
                TabSimb.inserir_elemento(variavel.value, tipo, "null", index, False, pilhaEscopos[-1], False, variavel.linha)

    def declaracao_variaveis(self, filho, TabSimb):
        resultado = self.get_no_folhas_para_variaveis(filho.child[1])
        lista_variaveis = resultado[0]
        index_valor = resultado[1]
        index_tipo = resultado[2]
        tipo = filho.child[0].value
        if index_tipo != "numero_int" and index_valor != None:
            print("Linha:["+str(lista_variaveis[0].linha)+"] Erro: índice de array '" + str(lista_variaveis[0].value) + "' não é um inteiro")
        else:
            self.declara_variaveis_na_tabela_de_simbolos(lista_variaveis, tipo, index_valor, TabSimb)


class ListaFuncoes():
    def __init__(self, nome, tipo_retorno, lista_paramentros, foi_retornada, escopo, used, escopo_pai, linha=None):
        self.nome = nome
        self.tipo_retorno = tipo_retorno
        self.lista_paramentros = lista_paramentros
        self.escopo = escopo
        self.escopo_pai = escopo_pai
        self.foi_retornada = foi_retornada
        self.used = used
        self.linha = linha


class TabelaSimbolos():
    TemPrincipal = False

    def __init__(self):
        self.lista_elementos = []
        self.lista_funcoes = []

    def pega_lista_funcoes(self):
        return self.lista_funcoes

    def inserir_elemento(self, nome, tipo, valor, indice, used, Escopo, ehParametro, linha=None):
        self.lista_elementos.append(Elemento(nome, Escopo, tipo, valor, indice, used, ehParametro, linha))

    def inserir_funcao(self, nome, tipo_retorno, foi_retornada, lista_paramentros, used, linha=None):
        escopo_pai = pilhaEscopos[-1]
        pilhaEscopos.append(nome)
        self.lista_funcoes.append(ListaFuncoes(nome, tipo_retorno, lista_paramentros, foi_retornada, pilhaEscopos[-1], used, escopo_pai, linha))

    def print_pilha(self):
        print("### PILHA DE ESCOPOS ###")
        for elemento in pilhaEscopos:
            print(elemento)

    def print_tabela_simbolos(self):
        print("### TABELA DE SIMBOLOS ###")
        for e in self.lista_elementos:
            if(e.indice):
                print("Tipo: " + str(e.tipo) + " Nome: " + str(e.nome) + " Indice: " + str(e.indice) +
                      " Valor: " + str(e.valor) + " Escopo: " + str(e.escopo) + " Usada: " + str(e.used))
            else:
                print("Tipo: " + str(e.tipo) + " Nome: " + str(e.nome) + " Valor: " +
                      str(e.valor) + " Escopo: " + str(e.escopo) + " Usada: " + str(e.used))

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
            if f.escopo_pai != "global":
                print("     + ----> Nome: " + f.nome + " Escopo: " + str(f.escopo) + " Escopo_PAI: " +  str(f.escopo_pai))
            else:
                print("Nome: " + f.nome + " Lista_Parametros: " + str(f.lista_paramentros) + " Tipo_Retorno: " + str(f.tipo_retorno) + " Escopo: " + str(f.escopo) + " Escopo_PAI: " + str(f.escopo_pai) + " Foi_Retornada: " + str(f.foi_retornada))

    def conferir_variaveis_usadas(self):
        if self.lista_elementos:
            for elemento in self.lista_elementos:
                if elemento.used == False:
                    print ("Linha:["+str(elemento.linha)+"] Aviso: Variável '" + str(elemento.nome) +"' declarada e não utilizada")

    def conferir_funcoes_declaradas(self):
        for f in self.lista_funcoes:
            if(f.foi_retornada == False):
                if f.tipo_retorno != "vazio":
                    print("Erro: Função '" + str(f.nome) + "' deveria retornar '" + str(f.tipo_retorno) + "', mas retorna vazio")
            if(f.used == False and f.nome != "principal"):
                print("Aviso: Função '"+str(f.nome)+"' declarada, mas não utilizada")
            

class Elemento():
    def __init__(self, nome, escopo, tipo, valor, indice, used, ehParametro, linha=None):
        self.nome = nome
        self.escopo = escopo
        self.tipo = tipo
        self.valor = valor
        self.used = used
        self.indice = indice
        self.ehParametro = ehParametro
        self.linha = linha
        

    def set_uso(self, elemento, usado):
        if(elemento):
            elemento.used = usado
        else:
            print("Erro: Variavel ainda não declarada")
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
    TabSimb.conferir_funcoes_declaradas()

    print("")
    print("")
    TabSimb.print_tabela_simbolos()
    TabSimb.print_tabela_funcoes()
    TabSimb.print_pilha()

    #print_tree(root.ps, dot)
    #print(dot.source)
    #dot.render('PrintArvore/Saida'+str(sys.argv[1])+str(now.day)+'-'+str(now.month)+'-' + str(now.year)+'h' + str(now.hour)+'m'+str(now.minute)+'s'+str(now.second)+'.gv.pdf', view=True)
