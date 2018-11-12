### Rafael Menzes Barboza, RA: 1817485 ###
from syn import * ## importar o arquivo syn.py
global pilhaEscopos
pilhaEscopos = ['global']

class Verifica_Arvore():
    def andar(self, raiz, TabSimb):
        if raiz and len(raiz.child)>=1:
            for filho in raiz.child:
                if filho.type == "declaracao_variaveis":
                   self.declaracao_variaveis(filho, TabSimb)
                elif filho.type == "declaracao_funcao":
                    self.declaracao_funcao(filho, TabSimb)
                elif filho.type == "expressao":
                    self.expressao(filho, TabSimb)
                elif filho.type == "retorna":
                    self.retorna(filho, TabSimb)
                elif filho.type == "chamada_funcao":
                    self.chamada_funcao(filho, TabSimb)
               # elif filho.value == "fim":
               #    self.fecha_escopo(filho)
                    
                if not isinstance(filho, Tree): return
                self.andar(filho, TabSimb)
        else:
            return
        
    def declaracao_funcao(self, no,  TabSimb):
        if no.type == "declaracao_funcao":
            if len(no.child) > 1:                     #Se existe tipo de retorno definido 
                nome_funcao = no.child[1].value
                tipo_funcao = no.child[0].value     
                lista_paramentros = self.cabecalho(no.child[1])
                TabSimb.verifica_declaracao_funcao(nome_funcao)
                TabSimb.inserir_funcao(nome_funcao, tipo_funcao, tipo_funcao, False, lista_paramentros)
            else:                                     #Se o tipo de retorno é void
                nome_funcao = no.child[0].value
                tipo_funcao = 'void'
                lista_paramentros = self.cabecalho(no.child[0])
                TabSimb.verifica_declaracao_funcao(nome_funcao)
                TabSimb.inserir_funcao(nome_funcao, tipo_funcao, tipo_funcao, False, lista_paramentros)
                
                

    def cabecalho(self, no):
        x = []
        if no.type == "cabecalho":
            self.pega_lista_parametros(no.child[0], x)
            return x

    def atribuicao(self, filho, TabSimb):
        if(filho.type == "atribuicao"):
            if(len(filho.child[0].child)>=1): 
                var = filho.child[0].value
                indice = self.str_to_number(self.ir_para_folha(filho.child[0]))
                valor = self.ir_para_folha(filho.child[1])
                if(str(type(indice)) == "<class 'int'>"):
                    TabSimb.atribuicao_elemento(var, valor, TabSimb)
                else:
                    print("Erro: índice de array " + var + " não inteiro")
                    exit(1)
            else:
                var = filho.child[0].value
                valor = self.ir_para_folha(filho.child[1])
                TabSimb.atribuicao_elemento(var, valor, TabSimb)


    def expressao_logica(self, filho, TabSimb):
        if filho.type == "expressao_logica":
            var1 = self.ir_para_folha(filho.child[0])
            var2 = self.ir_para_folha(filho.child[2])
            #operador_logico = self.ir_para_folha(filho.child[1])
            e_var1 = TabSimb.find_elemento(var1, None)
            e_var2 = TabSimb.find_elemento(var2, None)
            e_var1.set_uso(e_var1, True)
            e_var2.set_uso(e_var2, True)
            if e_var1.get_tipo(e_var1) != e_var2.get_tipo(e_var2):
                print("Warning: elementos de tipos diferentes na expressão logica (esta sendo realizado um parse)")
                e_var2.set_tipo(e_var2, e_var1.get_tipo(e_var1))



    def expressao_unaria(self, filho, TabSimb):
        if filho.type == "expressao_unaria":
            op_unitario = filho.child[0].value
            var = self.ir_para_folha(filho.child[1])
            elemento = TabSimb.find_elemento(var)
            TabSimb.set_sinal(elemento, op_unitario)
            print(op_unitario + var)

    def expressao_multiplicativa(self, filho, TabSimb):
        if filho.type == "expressao_multiplicativa":
            var1 = self.ir_para_folha(filho.child[0])
            var2 = self.ir_para_folha(filho.child[2])
            #op_multiplicativo = filho.child[1].value
            e_var1 = TabSimb.find_elemento(var1, None)
            e_var2 = TabSimb.find_elemento(var2, None)
            e_var1.set_uso(e_var1, True)
            e_var2.set_uso(e_var2, True)
            if e_var1.get_tipo(e_var1) != e_var2.get_tipo(e_var2):
                print("Warning: elementos de tipos diferentes na expressão multiplicativa (esta sendo realizado um parse)")
                e_var2.set_tipo(e_var2, e_var1.get_tipo(e_var1))

    def expressao_simples(self, filho, TabSimb):
        if filho.type == "expressao_simples":
                var1 = self.ir_para_folha(filho.child[0])
                var2 = self.ir_para_folha(filho.child[2])
                #op_relacional = filho.child[1].value
                e_var1 = TabSimb.find_elemento(var1, None)
                e_var2 = TabSimb.find_elemento(var2, None)
                e_var1.set_uso(e_var1, True)
                e_var2.set_uso(e_var2, True)
                if e_var1.get_tipo(e_var1) != e_var2.get_tipo(e_var2):
                    print("Warning: elementos de tipos diferentes na expressão (esta sendo realizado um parse)")
                    e_var2.set_tipo(e_var2, e_var1.get_tipo(e_var1))

    def i(self,string):
        try:
            int(string)
            return 0
        except ValueError:
            float(string)
            return 1

    def expressao_aditiva(self, filho, TabSimb):
        if filho.type == "expressao_aditiva":
                var1 = self.ir_para_folha(filho.child[0])
                var2 = self.ir_para_folha(filho.child[2])
                #op_aditivo = filho.child[1].value
                if self.i(var1) != 0 and self.i(var1) !=1 : 
                    e_var1 = TabSimb.find_elemento(var1)
                    e_var1.set_uso(e_var1, True)
                else:
                    e_var1 = self.str_to_number(var1)
                if self.i(var2) != 0 and self.i(var2) !=1: 
                    e_var2 = TabSimb.find_elemento(var2)
                    e_var2.set_uso(e_var2, True)
                else:
                    e_var2 = self.str_to_number(var2)


    def ir_para_folha(self, filho):
        if len(filho.child) <= 0:
            return filho.value
        else:
            return self.ir_para_folha(filho.child[0])

    def verificar_se_ha_chamada_funcao(self, filho):
        if filho.type == "chamada_funcao":
            lista = []
            lista.append(filho.value)
            lista.append(filho.child[0].value)
            return lista
        else:
            return self.verificar_se_ha_chamada_funcao(filho.child[0])

    def expressao(self, filho, TabSimb):
        if filho.type == "expressao":
            if filho.child[0].type == "atribuicao":
                self.atribuicao(filho.child[0], TabSimb)
            elif filho.child[0].type == "expressao_logica" and len(filho.child[0].child)>1 :
                self.expressao_logica(filho.child[0], TabSimb)
            elif filho.child[0].child[0].type == "expressao_simples" and len(filho.child[0].child[0].child)>1 :
                self.expressao_simples(filho.child[0].child[0], TabSimb)
            elif filho.child[0].child[0].child[0].type == "expressao_aditiva" and len(filho.child[0].child[0].child[0].child)>1 :
                self.expressao_aditiva(filho.child[0].child[0].child[0], TabSimb)
            elif filho.child[0].child[0].child[0].child[0].type == "expressao_multiplicativa" and len(filho.child[0].child[0].child[0].child[0].child)>1 :
                self.expressao_multiplicativa(filho.child[0].child[0].child[0].child[0], TabSimb)
            elif filho.child[0].child[0].child[0].child[0].child[0].type == "expressao_unaria" and len(filho.child[0].child[0].child[0].child[0].child[0].child)>1 :
                self.expressao_unaria(filho.child[0].child[0].child[0].child[0].child[0], TabSimb)

    
   
    def pega_lista_parametros(self, no, x):
        if no.type == "tipo":
            x.append(no.value)
        else:
            for filho in no.child:
                self.pega_lista_parametros(filho, x)
    
    def declaracao_variaveis(self, no, TabSimb):
        if no.type == "declaracao_variaveis":
            x = []
            tipo = self.pega_tipo_variavel(no)
            self.pega_nome_variavel(no, x, tipo, TabSimb)
            for variavel in x:
                TabSimb.inserir_elemento(variavel, tipo, "null", '' ,False)

    def fecha_escopo(self, no):
        if(no.value == "fim"):
            pilhaEscopos.pop()

    #PASSA O NO E RETORNA O TIPO DAS VARIAVEIS DA SUB-ARVORE DEPOIS DE (delaracao_variaveis)
    def pega_tipo_variavel(self, no):
        if no:
            for filho in no.child:
                if(filho.type == "tipo"):
                    return filho.value
                self.pega_tipo_variavel(filho)

    
    #PASSA O NO E RETORNA UMA LISTA COM AS VARIAVEIS DA SUB-ARVORE DEPOIS DE (delaracao_variaveis)    
    def pega_nome_variavel(self, no, x, tipo, TabSimb):
        if no:
            for filho in no.child:
                if(filho.type == "var"):
                    if len(filho.child) >= 1:
                        self.declaracao_vetor(filho.value, tipo, self.ir_para_folha(filho.child[0]), TabSimb)
                    else:
                        x.append(filho.value)
                    
                self.pega_nome_variavel(filho, x, tipo, TabSimb)
    
    def retorna(self, no, TabSimb):
        if no.type == "retorna":
            ultima_funcao = TabSimb.lista_funcoes[-1]
            ultima_funcao.foi_retornada = True
            var = self.ir_para_folha(no.child[0])
            if self.i(var) != 0 and self.i(var) !=1:
                elemento = TabSimb.find_elemento(var)
                print(str(elemento))
                if(elemento):
                    elemento.set_uso(elemento, True)
                    if ultima_funcao.valor_retorno == elemento.tipo:
                        print(str(ultima_funcao.valor_retorno))
                    else:
                        print ("Aviso: O tipo de Retorno nao é o mesmo da declaração da função")
                else:
                    print ("Erro: A variavel '" + var + "' ainda não foi declarada")
                    exit(1)
            
    
    def chamada_funcao(self, no, TabSimb):
        if no.type == "chamada_funcao":
            nome = no.value
            lista_arg = no.child[0].value
            funcao = TabSimb.find_funcao(nome)
            if(funcao != None):
                if (len(funcao.lista_paramentros) > len(lista_arg)):
                    print("Erro: Chamada à função '" + nome + "' com número de parâmetros menor que o declarado")
                    exit(1)
                elif (len(funcao.lista_paramentros) < len(lista_arg)):
                    print("Erro: Chamada à função '" + nome + "' com número de parâmetros maior que o declarado")
                    exit(1)
            else:
                print("Erro: Chamada da função '" + nome + "' que não foi declarada")
                exit(1)
            

                
    def str_to_number(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def declaracao_vetor(self, nome, tipo, indice, TabSimb):
        n_indice = self.str_to_number(indice)
        if(str(type(n_indice)) == "<class 'int'>"):
            TabSimb.inserir_elemento(nome, tipo, 'null', indice, False)
        else:
            print("Erro: índice de array " + nome + " não inteiro")
            exit(1)

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
        print ("### PILHA DE ESCOPOS ###")
        for elemento in pilhaEscopos:
            print(elemento)

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
    
    
    def verifica_declaracao_funcao(self, nome_funcao):
        if nome_funcao == "principal":
            self.TemPrincipal = True
        for funcao in self.lista_funcoes:
            if(funcao.nome == nome_funcao):
                print ("Erro: Existem funçoes duplicadas no programa")
                exit(1)
    
    def str_to_number(self, s):
        try:
            int(s)
            return "<class 'int'>"
        except ValueError:
            float(s)
            return "<class 'float'>"
    
    def atribuicao_elemento(self, var, valor, TabSimb):
        print(var)
        elemento = self.find_elemento(var)
        if elemento:
            if(elemento.get_tipo(elemento) == "inteiro" and self.str_to_number(valor) != "<class 'int'>"):
                print ("Aviso: Atribuição de tipos distintos '" + str(elemento.nome) + "' " + str(elemento.tipo) + " e '" + str(valor) + "' flutuante") 
                elemento.set_uso(elemento, True)
                elemento.set_valor(elemento, valor, TabSimb)
            elif(elemento.get_tipo(elemento) == "flutuante" and self.str_to_number(valor) != "<class 'float'>"):
                print ("Aviso: Atribuição de tipos distintos '" + str(elemento.nome) + "' " + str(elemento.tipo) + " e '" + str(valor) + "' inteiro") 
                elemento.set_uso(elemento, True)
                elemento.set_valor(elemento, valor, TabSimb)
            else:
                elemento.set_uso(elemento, True)
                elemento.set_valor(elemento, valor, TabSimb)
        else:
            print ("error: A variavel que deseja atribuir nao foi declarada em nenhum escopo, nem global nem local")

    def set_sinal(self, elemento, op_unitario):
        if(elemento.valor == 'null'):
            print ("ERRO: Você ainda nao atribuio nenhum valor a esta variavel.")
        else:
            if elemento.get_tipo(elemento) == "inteiro":
                elemento.valor = int(elemento.valor) * int(op_unitario) 
                print(elemento.valor)
            elif elemento.get_tipo(elemento) == "flutuante":
                elemento.valor = float(elemento.valor) * float(op_unitario) 
                print(elemento.valor)

    def conferir_variaveis_usadas(self):
        if (self.lista_elementos):
            for elemento in self.lista_elementos:
                if elemento.used == False:
                    print ("Aviso: Variável '" + elemento.nome +"' declarada e não utilizada")

    def conferir_funcoes_declaradas(self):
        for f in self.lista_funcoes:
            if(f.foi_retornada == False):
                print("Erro: Função " + f.nome + " deveria retornar " + f.tipo_retorno + ", mas retorna vazio")
                exit(1)
    
    def print_tabela_simbolos(self):
        print("### TABELA DE SIMBOLOS ###")
        for e in self.lista_elementos:
            if(e.indice):
                print("Tipo: " + e.tipo + " Nome: " + e.nome + " Indice: " + e.indice + " Valor: " + str(e.valor) + " Escopo: " + e.escopo + " Usada: " + str(e.used))
            else:
                print("Tipo: " + e.tipo + " Nome: " + e.nome + " Valor: " + str(e.valor) + " Escopo: " + e.escopo + " Usada: " + str(e.used))
    
    def print_tabela_funcoes(self):
        print("### TABELA DE FUNCOES ###")
        for f in self.lista_funcoes:
                print("Nome: " + f.nome + " Lista_Parametros: " + str(f.lista_paramentros) + " Tipo_Retorno: " + str(f.tipo_retorno) + " Valor_Retorno: " + str(f.valor_retorno) + " Escopo: " + str(f.escopo))
        

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
        if(valor.isdigit() == False):
            var = TabSimb.find_elemento(valor)
            elemento.valor = var.valor
        else:
            elemento.valor = valor
            

    def get_tipo(self, elemento):
        return elemento.tipo

    def set_tipo(self, elemento, tipo):
        elemento.tipo = tipo


if __name__ == '__main__':
    Sintatico = Verifica_Arvore()
    root = Syn()
    TabSimb = TabelaSimbolos()
    Sintatico.andar(root.ps, TabSimb)
    TabSimb.conferir_variaveis_usadas()     #VERIFICA SE AS VARIAVEIS SAO USADAS OU NAO
    TabSimb.conferir_funcoes_declaradas()

    if(TabSimb.TemPrincipal == False):      #VERIFICA SE TEM A FUNÇÃO PRINCIPAL
        print ("Erro: Função principal não declarada")
        exit(1)
    else:
        TabSimb.print_pilha()
        TabSimb.print_tabela_simbolos()
        TabSimb.print_tabela_funcoes()
        
    
    