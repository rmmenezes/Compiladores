### Rafael Menzes Barboza, RA: 1817485 ###
from graphviz import Digraph
import sys
from datetime import datetime
from poda import *
from llvmlite import ir
from lex import Lex
import sys


class Gerador_TOP:
    def __init__(self):
        self.builder = None
        self.funcao_main = None
        self.lista_ponteiros_variaveis = []

    def andar(self, raiz, modulo):
            if raiz:
                for filho in raiz.child:
                    if filho.type == "declaracao_variaveis":
                        self.declaracao_variaveis(raiz, filho, modulo)
                    if filho.type == "declaracao_funcao":
                        self.declaracao_funcao(raiz, filho, modulo)
                    if filho.type == "atribuicao":
                        self.atribuicao(raiz, filho, modulo)
                    if not isinstance(filho, Tree):
                        return
                    self.andar(filho, modulo)
            else:
                return

    def resolve_expressao(self, filho, modulo):
        # O no filho é do tipo EXPRESSAO ↑
        if len(filho.child) == 1:
            if filho.child[0].type == "var":
                valor_da_atribuicao = filho.child[0].value
                i = 0
                while i < len(self.lista_ponteiros_variaveis):
                    if str(self.lista_ponteiros_variaveis[i].name) == str(valor_da_atribuicao):
                        valor_da_atribuicao = self.lista_ponteiros_variaveis[i]
                    i = i + 1
                varTemp = self.builder.load(valor_da_atribuicao, name='varTemp', align=4)
                return varTemp
            elif filho.child[0].type == "numero_int":
                varTemp = ir.Constant(ir.IntType(32), int(filho.child[0].value))
                return varTemp
            elif filho.child[0].type == "numero_float":
                varTemp = ir.Constant(ir.FloatType(), float(filho.child[0].value))
                return varTemp

        elif len(filho.child) == 3:
            filho_esquerda = filho.child[0]
            operador = filho.child[1]
            filho_direita = filho.child[2]
            # ----------------------------------------------------------- #
            if filho_direita.type == "var":
                i = 0
                while i < len(self.lista_ponteiros_variaveis):
                    if str(self.lista_ponteiros_variaveis[i].name) == str(filho_direita.value):
                        filho_direita = self.lista_ponteiros_variaveis[i]
                    i = i + 1
                varTempRight = self.builder.load(filho_esquerda, name='varTempLeft', align=4)
            elif filho_direita.type == "numero_int":
                varTempRight = ir.Constant(ir.IntType(32), int(filho_direita.value))
            elif filho_direita.type == "numero_float":
                varTempRight = ir.Constant(ir.FloatType(), float(filho_direita.value))
            # ----------------------------------------------------------- #
           
            # ----------------------------------------------------------- #
            if filho_esquerda.type == "var":
                i = 0
                while i < len(self.lista_ponteiros_variaveis):
                    if str(self.lista_ponteiros_variaveis[i].name) == str(filho_esquerda.value):
                        filho_esquerda = self.lista_ponteiros_variaveis[i]
                    i = i + 1
                varTempLeft = self.builder.load(filho_esquerda, name='varTempLeft', align=4)
            elif filho_esquerda.type == "numero_int":
                varTempLeft = ir.Constant(ir.IntType(32), int(filho_esquerda.value))
            elif filho_esquerda.type == "numero_float":
                varTempLeft = ir.Constant(ir.FloatType(), float(filho_esquerda.value))
            # ----------------------------------------------------------- #
            
            if operador.type == "operador_soma":
                if operador.value == "+":
                    varTempAdd = self.builder.add(varTempLeft, varTempRight, name="varTempAdd")
                    return varTempAdd
                elif operador.value == "-":
                    varTempSub = self.builder.sub(varTempLeft, varTempRight, name="varTempSub")
                    return varTempSub

    def atribuicao(self, raiz, filho, modulo):
        variavel = filho.child[0].value
        i = 0
        while i < len(self.lista_ponteiros_variaveis):
            if self.lista_ponteiros_variaveis[i].name == variavel:
                variavel = self.lista_ponteiros_variaveis[i]
            i = i + 1
        # ↑ O codigo a cima faz o papel de encontrar a variavel ↑ 
        resultado = self.resolve_expressao(filho.child[1], modulo)
        self.builder.store(resultado, variavel)


    def declaracao_funcao(self, raiz, filho, modulo):
        tipo = filho.child[0].value
        if filho.child[1].value == "principal":
            self.llvm_declaracao_funcao_principal(filho.value, tipo, modulo)


    def llvm_declaracao_funcao_principal(self, nome, tipo, modulo):
        if tipo == "inteiro":
            tipo_de_retorno = ir.IntType(32)
        elif tipo == "flutuante":
            tipo_de_retorno = ir.FloatType()

        funcao_main = ir.FunctionType(tipo_de_retorno, ())
        self.funcao_main = ir.Function(modulo, funcao_main, name='main')
        bloco_de_entrada = self.funcao_main.append_basic_block('main.entry')
        self.builder = ir.IRBuilder(bloco_de_entrada)
        valor_de_retorno = self.builder.alloca(tipo_de_retorno, name='return')
        #bloco_de_saida = self.funcao_main.append_basic_block('main.exit')
        


    def declaracao_variaveis(self, raiz, filho, modulo):
        tipo = filho.child[0].value
        if raiz.type == "lista_declaracoes":
            for filhos in filho.child[1].child:
                self.llvm_declaracao_variavel_global(tipo, filhos.value, modulo)
            
        else:
            for filhos in filho.child[1].child:
                self.llvm_declaracao_variavel_local(tipo, filhos.value, modulo)
            

    def llvm_declaracao_variavel_global(self, tipo, variavel_arg, modulo):
        if tipo == "inteiro":
            variavel = ir.GlobalVariable(modulo, ir.IntType(32), variavel_arg)
            variavel.initializer = ir.Constant(ir.IntType(32), 0)
            variavel.linkage = "common"
            variavel.align = 4
        elif tipo == "flutuante":
            variavel = ir.GlobalVariable(modulo, ir.FloatType(), variavel_arg)
            variavel.initializer = ir.Constant(ir.FloatType(), 0.0)
            variavel.linkage = "common"
            variavel.align = 4
        self.lista_ponteiros_variaveis.append(variavel)

    def llvm_declaracao_variavel_local(self, tipo, variavel_arg, modulo):
        if tipo == "inteiro":
            variavel = self.builder.alloca(ir.IntType(32), name=variavel_arg)
            variavel.align = 4
        elif tipo == "flutuante":
            variavel = self.builder.alloca(ir.FloatType(), name=variavel_arg)
            variavel.align = 4
        self.lista_ponteiros_variaveis.append(variavel)

if __name__ == '__main__':
    now = datetime.now()
    root = Syn()                        # Chama o analisador Sintatico
    Run(root.ps)                        # Poda a arvore
    dot = Digraph(comment='TREE')       # Abaixo é o processo de impressão
    Gerador = Gerador_TOP()

    NomeProg = sys.argv[1]
    modulo = ir.Module(NomeProg)

    Gerador.andar(root.ps, modulo)
    arquivo = open(NomeProg+'.ll', 'w')
    arquivo.write(str(modulo))
    arquivo.close()
    print(modulo)