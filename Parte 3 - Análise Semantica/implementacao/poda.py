#### PAC_MAN.PY
from syn import Syn
from syn import Tree
from lex import Lex
from graphviz import Digraph
### Rafael Menzes Barboza, RA: 1817485 ###
from graphviz import Digraph
import sys
from datetime import datetime

def pacMan(node): 
    if node != None:
        if not isinstance(node, Tree): return
        for son in node.child:
            pacMan(son)
            if son.type == 'expressao_logica':                  #tira caminho gigante que tinha
                leafs = []                                      #ate encontrar um numero, var ou função
                getLeafs(son, leafs)
                for l in leafs:
                    node.child.append(l) #deixar append com recursão em cima
                node.child.remove(son)
            if son.type == 'vazio' and node.type == 'corpo': #remove vazio para o caso: 
                node.child.remove(son)
            if son.type == 'declaracao':
                for i in son.child:
                    node.child.append(i) #deixar append com recursão em cima
                node.child.remove(son)
            if son.type == 'expressao' and (node.type == 'indice' or node.type == 'escreva'):
                for i in son.child:
                    node.child.append(i)
                node.child.remove(son)  #deixar append com recursão em cima
            for grand in son.child:
                if grand.type == 'atribuicao' and son.type == 'expressao' and node.type == 'atribuicao':
                    for g in grand.child:
                        node.child.append(g)
                    node.child.remove(son)                    

                if node.type == 'corpo' and son.type == 'acao' and grand.type == 'expressao':
                    node.child.append(grand.child[0])
                    node.child.remove(son)
   
def removeTheSames(node):
    if node != None:
        if not isinstance(node, Tree): return
        for son in node.child:
            if son.type == node.type:                        #remove nós com mesmo nome em sequencia 
                for i in son.child:                          #(ação, listas de variaveis, etc)..
                    node.child.insert(0, i)
                node.child.remove(son)
                removeTheSames(node)
            if son.type == 'acao' and node.type == 'corpo':
                    for i in son.child:
                        node.child[node.child.index(son)] = i   
            removeTheSames(son)
        
def getLeafs(node, values=[]):
    if node:
        for son in node.child:
            if son.type == 'chamada_funcao':
                values.append(son)
                return
            if son.type == 'indice':
                return
            if son.value:
                values.append(son)
            getLeafs(son, values)

def TrimTree(node):
    pacMan(node)
    removeTheSames(node)  
            

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
        TrimTree(syn.ps)
        dot = Digraph(comment='TREE')
        print_tree(syn.ps, dot)
        print(dot.source)
        dot.render('PrintArvore/Saida'+str(sys.argv[1])+str(now.day)+'-'+str(now.month)+'-'+ str(now.year)+'h'+ str(now.hour)+'m'+str(now.minute)+'s'+str(now.second)+'.gv.pdf', view=True)
    else:
        print("Erro de arquivo XD!")