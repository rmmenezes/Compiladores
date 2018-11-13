### Rafael Menzes Barboza, RA: 1817485 ###
from syn import * ## importar o arquivo syn.py

root = Syn()

class Sin():
    def andar(self, raiz):
        if raiz:
            for filho in raiz.child:
                print(filho)
                if not isinstance(filho, Tree): return
                self.andar(filho)



if __name__ == '__main__':
    Sint = Sin()
    Sint.andar(root.ps)

