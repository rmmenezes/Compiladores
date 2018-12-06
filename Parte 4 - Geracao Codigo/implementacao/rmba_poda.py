### Rafael Menzes Barboza, RA: 1817485 ###
from syn import Syn
from syn import Tree
from lex import Lex
from graphviz import Digraph
from graphviz import Digraph
import sys
from datetime import datetime

def funcao_poda(raiz):
    if raiz != None:
        for no in raiz.child:
            if not isinstance(no, Tree): return
            if no.type == "expressao":
                lista_de_filhos = []
                desce_ate_bifurcar_ou_ate_no_fim(no, lista_de_filhos)
                atribuir_lista_de_filhos_ao_no(no, lista_de_filhos)
            funcao_poda(no)
        

def atribuir_lista_de_filhos_ao_no(no, lista_de_filhos):
    for filhos in no.child:
        no.child.remove(filhos)
    
    for filhos in lista_de_filhos:
        no.child.append(filhos)


def desce_ate_bifurcar_ou_ate_no_fim(no, lista_de_filhos):
    if len(no.child) == 0:
        print(no.value)
        lista_de_filhos.append(no)

    if len(no.child) > 0:
        for filho in no.child:
            desce_ate_bifurcar_ou_ate_no_fim(filho, lista_de_filhos)

def print_tree(node, dot, i="0", pai=None):
    if node != None:
        filho = str(node) + str(i)
        dot.node(filho, str(node))
        if pai: dot.edge(pai, filho)
        j = "0"
        if not isinstance(node, Tree): return
        for no in node.child:
            j+="1"
            print_tree(no, dot, i+j, filho) 


if __name__ == '__main__':
    now = datetime.now()
    if len(sys.argv) > 1:
        syn = Syn()
        funcao_poda(syn.ps)
        dot = Digraph(comment='TREE')
        print_tree(syn.ps, dot)
        dot.render('PrintArvore/Saida'+str(sys.argv[1])+str(now.day)+'-'+str(now.month)+'-'+ str(now.year)+'h'+ str(now.hour)+'m'+str(now.minute)+'s'+str(now.second)+'.gv.pdf', view=True)
    else:
        print("Erro de arquivo XD!")