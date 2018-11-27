### Rafael Menzes Barboza, RA: 1817485 ###
from syn import * ## importar o arquivo syn.py

class Sin():
    def andar(self, raiz):
        if raiz:
            for filho in raiz.child:
                # print(filho)
                self.andar(filho)

    
class Escopo():
    def __init__(self, nome, pai_escopo):
        self.nome = nome
        self.lista_escopo = []
        self.lista_elementos = []
        self.pai_escopo = pai_escopo
    
    def inserir_escopo(self, escopo):
        self.lista_escopo.append(escopo)
    
    def printa_nome_filhos(self):
        for f in self.lista_escopo:
            print(f.nome)
    
    def printa_nome_elementos(self):
        for f in self.lista_elementos:
            print("Nome: ",f.nome, "Tipo: ", f.tipo)
    
    def inserir_elemento(self, nome, tipo=None, valor=None, used=None):
        self.lista_elementos.append(Elemento(nome, tipo, valor, used))

    def print_var_pai(self):
        self.pai_escopo.printa_nome_elementos()

class Elemento():
    def __init__(self, nome, tipo = None, valor=None, used=None):
        self.nome = nome
        if tipo:
            self.tipo = tipo
        else:
            self.tipo = "nao tem tipo"
        if valor:
            self.valor = valor
        else:
            self.valor = ''
        self.used = 'nao usado'
    




if __name__ == '__main__':
    Sint = Sin()
    root = Syn()
    # sua arvore é o root.ps
    #print(root.ps.child[0].child[0].child[0].child[0])
    
    rafael = Escopo("global", None)
    rafael.inserir_elemento("a", "inteiro")
    bubble = Escopo("bubble", rafael)
    #bubble.printa_nome_elementos()
    rafael.inserir_escopo(bubble)
    #rafael.printa_nome_filhos()
    #rafael.printa_nome_elementos()
    bubble.print_var_pai()
