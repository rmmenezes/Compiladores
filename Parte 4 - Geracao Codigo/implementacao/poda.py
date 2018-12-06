### Rafael Menzes Barboza, RA: 1817485 ###
from syn import Syn
from syn import Tree
from lex import Lex
from graphviz import Digraph
from graphviz import Digraph
import sys
from datetime import datetime

def poda_arvore(no):
    if no != None:
        if not isinstance(no, Tree): return
        for filho in no.child:
            poda_arvore(filho)
            if filho.type == "expressao_logica":                 
                lfs = []
                get(filho, lfs)
                for l in lfs:
                    no.child.append(l)
                no.child.remove(filho)
            if filho.type == "vazio" and no.type == "corpo":
                no.child.remove(filho)
            if filho.type == "declaracao":
                for i in filho.child:
                    no.child.append(i)
                no.child.remove(filho)
            if filho.type == "expressao" and (no.type == "indice" or no.type == "escreva"):
                for i in filho.child:
                    no.child.append(i)
                no.child.remove(filho)
            for grand in filho.child:
                if grand.type == "atribuicao" and filho.type == "expressao" and no.type == "atribuicao":
                    for g in grand.child:
                        no.child.append(g)
                    no.child.remove(filho)                    
                if no.type == "corpo" and filho.type == "acao" and grand.type == "expressao":
                    no.child.append(grand.child[0])
                    no.child.remove(filho)
   
def remove_2(no):
    if no != None:
        if not isinstance(no, Tree): return
        for filho in no.child:
            if filho.type == no.type:
                for i in filho.child:
                    no.child.insert(0, i)
                no.child.remove(filho)
                remove_2(no)
            if filho.type == "acao" and no.type == "corpo":
                    for i in filho.child:
                        no.child[no.child.index(filho)] = i   
            remove_2(filho)
        
def get(no, values=[]):
    if no:
        for filho in no.child:
            if filho.type == "chamada_funcao":
                values.append(filho)
                return
            if filho.type == "indice":
                return
            if filho.value:
                values.append(filho)
            get(filho, values)

def Run(no):
    poda_arvore(no)
    remove_2(no)  
            

def print_tree(no, dot, i="0", pai=None):
    if no != None:
        filho = str(no) + str(i)
        dot.no(filho, str(no))
        if pai: dot.edge(pai, filho)
        j = "0"
        if not isinstance(no, Tree): return
        for no in no.child:
            j+="1"
            print_tree(no, dot, i+j, filho) 

if __name__ == "__main__":
    now = datetime.now()
    if len(sys.argv) > 1:
        syn = Syn()
        Run(syn.ps)
        dot = Digraph(comment="TREE")
        print_tree(syn.ps, dot)
        print(dot.source)
        dot.render("PrintArvore/Saida"+str(sys.argv[1])+str(now.day)+"-"+str(now.month)+"-"+ str(now.year)+"h"+ str(now.hour)+"m"+str(now.minute)+"s"+str(now.second)+".gv.pdf", view=True)
    else:
        print("Erro de arquivo XD!")