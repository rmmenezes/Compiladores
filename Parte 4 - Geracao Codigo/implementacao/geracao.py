# -*- coding: utf-8 -*-
### Rafael Menzes Barboza, RA: 1817485 ###
from graphviz import Digraph
import sys
from datetime import datetime
from poda import *
from llvmlite import ir
from lex import Lex
import sys
from ctypes import CFUNCTYPE, c_int32

global_string_name = 0  

class Gerador_TOP:
    def __init__(self):
        self.builder = None
        self.funcao_main = None
        self.lista_ponteiros_variaveis = []
        self.lista_ponteiros_funcoes = []
        self.contador_se = 0
        self.conta_repita = 0
        self.leia = None

    def andar(self, raiz, modulo):
            if raiz:
                for filho in raiz.child:
                    if filho.type == "declaracao_variaveis":
                        self.llvm_declaracao_variavel_global(raiz, filho, modulo)
                    if filho.type == "declaracao_funcao":
                        self.declaracao_funcao(raiz, filho, modulo)
                    if not isinstance(filho, Tree): return
                    self.andar(filho, modulo)
            else:
                return

    def retorna(self, filho, modulo, builder):
        i = 0
        while i < len(self.lista_ponteiros_variaveis):
            if self.lista_ponteiros_variaveis[i].name == "return":
                retorna = self.builder.load(self.lista_ponteiros_variaveis[i], name="retorna", align=4)
            i = i + 1

        nome = self.lista_ponteiros_funcoes[-1].name
        bloco_de_saida = self.lista_ponteiros_funcoes[-1].append_basic_block('%s.end' % nome)
        builder.branch(bloco_de_saida)
        builder.position_at_end(bloco_de_saida)

        res = self.resolve_expressao(filho.child[0], modulo)
        i=0
        while i < len(self.lista_ponteiros_variaveis):
            if self.lista_ponteiros_variaveis[i].name == "return":
                variavel_de_retorno = self.lista_ponteiros_variaveis[i]
            i = i + 1
        builder.store(res, variavel_de_retorno)
        builder.ret(builder.load(variavel_de_retorno, name="ret"))

    
    def declaracao_funcao(self, raiz, filho, modulo):
        tipo_de_retorno = filho.child[0].value
        nome = filho.child[1].value
        self.llvm_declaracao_funcao(modulo, filho, nome, tipo_de_retorno)

    def llvm_declaracao_funcao(self, modulo, filho, nome, tipo_de_retorno):
        if nome == "principal":
            nome = "main"
        if tipo_de_retorno == "inteiro":
            tipo_de_retorno = ir.IntType(32)
        elif tipo_de_retorno == "flutuante":
            tipo_de_retorno = ir.FloatType()

        tipo_da_funcao = ir.FunctionType(tipo_de_retorno, [])
        funcao = ir.Function(modulo, tipo_da_funcao, name=nome)
        self.lista_ponteiros_funcoes.append(funcao)

        bloco_de_entrada = funcao.append_basic_block('%s.start' % nome)

        self.builder = ir.IRBuilder(bloco_de_entrada)

        retorna = self.builder.alloca(tipo_de_retorno, name='return')
        self.lista_ponteiros_variaveis.append(retorna)

        corpo = filho.child[1].child[1]
        self.resolve_corpo(corpo, modulo, self.builder)


    def resolve_corpo(self, raiz, modulo, builder):
        if raiz:
            for filho in raiz.child:
                if filho.type == "declaracao_variaveis":
                    self.llvm_declaracao_variavel_local(filho, builder)
                elif filho.type == "atribuicao":
                    self.atribuicao(filho, modulo, builder)
                elif filho.type == "se":
                    self.se(filho, modulo, builder)
                elif filho.type == "repita":
                    self.repita(filho, modulo, builder)
                elif filho.type == "leia":
                    self.leia_func(filho, modulo, builder)
                elif filho.type == "escreva":
                    self.escreva(filho, modulo, builder)
                elif filho.type == "retorna":
                    self.retorna(filho, modulo, builder)
                elif not isinstance(filho, Tree): return
                self.resolve_corpo(filho, modulo, builder)
        else:
            return


    def leia_func(self, filho, modulo, builder):
        for i in self.lista_ponteiros_variaveis:
            if i.name == filho.child[0].value:
                variavel = i
        leia = self.funcao_externa("scanf", modulo)

    def funcao_externa(self, name, modulo):
        func_type = ir.FunctionType(ir.IntType(32), (), var_args=True)
        return modulo.declare_intrinsic(name, (), func_type)

    def declara_string_global(self, module, string_parametro):
        typ = ir.ArrayType(ir.IntType(8), len(string_parametro))
        temp = ir.GlobalVariable(module, typ, name=str("scanf"))

    def chama_funcao(self, funcao, args):
        self.builder.call(funcao, args)

    def escreva(self, filho, modulo, builder):
        print("ESCREVA")

    def repita(self, filho, modulo, builder):
        repitatrue = self.lista_ponteiros_funcoes[-1].append_basic_block("repitatrue_"+str(self.conta_repita))
        repitaend = self.lista_ponteiros_funcoes[-1].append_basic_block("repitaend_"+str(self.conta_repita))

        corpo = filho.child[0]
        expressao = filho.child[1]

        filho_esquerda = expressao.child[0]
        operador = expressao.child[1]
        
        filho_direita = expressao.child[2]
        valor_filho_esquerda = expressao.child[0].value
        valor_filho_direita = expressao.child[2].value
        # ----------------------------------------------------------- #
        if filho_direita.type == "var":
            i = 0
            while i < len(self.lista_ponteiros_variaveis):
                if str(self.lista_ponteiros_variaveis[i].name) == valor_filho_direita:
                    filho_direita = self.lista_ponteiros_variaveis[i]
                i = i + 1
            varTempRight = self.builder.load(filho_direita, name='varTempLeft')
        elif filho_direita.type == "numero_int":
            varTempRight = ir.Constant(ir.IntType(32), int(filho_direita.value))
        elif filho_direita.type == "numero_float":
            varTempRight = ir.Constant(ir.FloatType(), float(filho_direita.value))
        # ----------------------------------------------------------- #
        # ----------------------------------------------------------- #
        if filho_esquerda.type == "var":
            i = 0
            while i < len(self.lista_ponteiros_variaveis):
                if str(self.lista_ponteiros_variaveis[i].name) == valor_filho_esquerda:
                    filho_esquerda = self.lista_ponteiros_variaveis[i]
                i = i + 1
            varTempLeft = self.builder.load(filho_esquerda, name='varTempLeft')
        elif filho_esquerda.type == "numero_int":
            varTempLeft = ir.Constant(ir.IntType(32), int(filho_esquerda.value))
        elif filho_esquerda.type == "numero_float":
            varTempLeft = ir.Constant(ir.FloatType(), float(filho_esquerda.value))
        # ----------------------------------------------------------- #   
        if operador.value == "=":
            operador = "==" 
        else:
            operador = operador.value    
        self.conta_repita = self.conta_repita + 1
        repita = self.builder.icmp_signed(operador, varTempLeft, varTempRight, name="if_"+str(self.contador_se))
        self.builder.branch(repitatrue)

        self.builder.position_at_start(repitatrue)
        self.resolve_corpo(corpo, modulo, builder)
        self.builder.position_at_end(repitatrue)
        self.builder.cbranch(repita, repitaend, repitatrue)
        self.builder.position_at_end(repitaend)

    def se(self, filho, modulo, builder):
        iftrue = self.lista_ponteiros_funcoes[-1].append_basic_block("iftrue_"+str(self.contador_se))
        iffalse = self.lista_ponteiros_funcoes[-1].append_basic_block("iffalse_"+str(self.contador_se))
        ifend = self.lista_ponteiros_funcoes[-1].append_basic_block("ifend_"+str(self.contador_se))

        expressao = filho.child[0]
        se_corpo1 = filho.child[1]
        se_corpo2 = filho.child[2]

        filho_esquerda = expressao.child[0]
        operador = expressao.child[1]
        filho_direita = expressao.child[2]
        valor_filho_esquerda = expressao.child[0].value
        valor_filho_direita = expressao.child[2].value
        # ----------------------------------------------------------- #
        if filho_direita.type == "var":
            i = 0
            while i < len(self.lista_ponteiros_variaveis):
                if str(self.lista_ponteiros_variaveis[i].name) == valor_filho_direita:
                    filho_direita = self.lista_ponteiros_variaveis[i]
                i = i + 1
            varTempRight = self.builder.load(filho_direita, name='varTempLeft')
        elif filho_direita.type == "numero_int":
            varTempRight = ir.Constant(ir.IntType(32), int(filho_direita.value))
        elif filho_direita.type == "numero_float":
            varTempRight = ir.Constant(ir.FloatType(), float(filho_direita.value))
        # ----------------------------------------------------------- #
        # ----------------------------------------------------------- #
        if filho_esquerda.type == "var":
            i = 0
            while i < len(self.lista_ponteiros_variaveis):
                if str(self.lista_ponteiros_variaveis[i].name) == valor_filho_esquerda:
                    filho_esquerda = self.lista_ponteiros_variaveis[i]
                i = i + 1
            varTempLeft = self.builder.load(filho_esquerda, name='varTempLeft')
        elif filho_esquerda.type == "numero_int":
            varTempLeft = ir.Constant(ir.IntType(32), int(filho_esquerda.value))
        elif filho_esquerda.type == "numero_float":
            varTempLeft = ir.Constant(ir.FloatType(), float(filho_esquerda.value))
        # ----------------------------------------------------------- #
        If = self.builder.icmp_signed(operador.value, varTempLeft, varTempRight, name="if_"+str(self.contador_se))
        self.builder.cbranch(If, iftrue, iffalse)
        self.builder.position_at_start(iftrue)
        self.resolve_corpo(se_corpo1, modulo, builder)
        self.builder.branch(ifend)
        self.builder.position_at_start(iffalse)
        self.resolve_corpo(se_corpo2, modulo, builder)
        self.builder.branch(ifend)
        self.builder.position_at_end(ifend)
        self.contador_se = self.contador_se + 1

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
                varTemp = self.builder.load(valor_da_atribuicao, name='varTemp')
                return varTemp
            elif filho.child[0].type == "numero_int":
                varTemp = ir.Constant(ir.IntType(32), filho.child[0].value)
                return varTemp
            elif filho.child[0].type == "numero_float":
                varTemp = ir.Constant(ir.FloatType(), filho.child[0].value)
                return varTemp

        elif len(filho.child) == 3:
            filho_esquerda = filho.child[0]
            operador = filho.child[1]
            filho_direita = filho.child[2]
            valor_filho_esquerda = str(filho_esquerda.value)
            valor_filho_direita = str(filho_direita.value)
            
            # ----------------------------------------------------------- #
            if filho_direita.type == "var":
                i = 0
                while i < len(self.lista_ponteiros_variaveis):
                    if str(self.lista_ponteiros_variaveis[i].name) == valor_filho_direita:
                        filho_direita = self.lista_ponteiros_variaveis[i]
                    i = i + 1
                varTempRight = self.builder.load(filho_direita, name='varTempLeft')
            elif filho_direita.type == "numero_int":
                varTempRight = ir.Constant(ir.IntType(32), int(filho_direita.value))
            elif filho_direita.type == "numero_float":
                varTempRight = ir.Constant(ir.FloatType(), float(filho_direita.value))
            # ----------------------------------------------------------- #
           
            # ----------------------------------------------------------- #
            if filho_esquerda.type == "var":
                i = 0
                while i < len(self.lista_ponteiros_variaveis):
                    if str(self.lista_ponteiros_variaveis[i].name) == valor_filho_esquerda:
                        filho_esquerda = self.lista_ponteiros_variaveis[i]
                    i = i + 1
                varTempLeft = self.builder.load(filho_esquerda, name='varTempLeft')
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
            

    def atribuicao(self,filho, modulo, builder):
        variavel = filho.child[0].value
        i = 0
        while i < len(self.lista_ponteiros_variaveis):
            if self.lista_ponteiros_variaveis[i].name == variavel:
                variavel = self.lista_ponteiros_variaveis[i]
            i = i + 1
        # ↑ O codigo a cima faz o papel de encontrar a variavel ↑ 
        resultado = self.resolve_expressao(filho.child[1], modulo)
        builder.store(resultado, variavel)
            
    def llvm_declaracao_variavel_global(self, raiz, filho, modulo):
        tipo = filho.child[0].value
        if raiz.type == "lista_declaracoes":
            for filhos in filho.child[1].child:         
                if tipo == "inteiro":
                    variavel = ir.GlobalVariable(modulo, ir.IntType(32), filhos.value)
                    variavel.initializer = ir.Constant(ir.IntType(32), 0)
                    variavel.linkage = "common"
                    variavel.align = 4
                elif tipo == "flutuante":
                    variavel = ir.GlobalVariable(modulo, ir.FloatType(), filhos.value)
                    variavel.initializer = ir.Constant(ir.FloatType(), 0.0)
                    variavel.linkage = "common"
                    variavel.align = 4
                self.lista_ponteiros_variaveis.append(variavel)

    def llvm_declaracao_variavel_local(self, filho, builder):
        tipo = filho.child[0].value
        for filhos in filho.child[1].child: 
            if tipo == "inteiro":
                variavel = builder.alloca(ir.IntType(32), name=filhos.value)
                variavel.align = 4
            elif tipo == "flutuante":
                variavel = builder.alloca(ir.FloatType(), name=filhos.value)
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
    arquivo = open(NomeProg+'.ll','w')
    arquivo.write(str(modulo))
    arquivo.close()
    print(modulo)