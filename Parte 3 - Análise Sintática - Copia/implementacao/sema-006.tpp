{Aviso: Variável 'b' declarada e não utilizada}
{Aviso: Atribuição de tipos distintos 'b' inteiro e 'c' flutuante}
{Aviso: Atribuição de tipos distintos 'a' flutuante e 'func' retorna inteiro}
{Erro: Função principal deveria retornar inteiro, mas retorna vazio}

inteiro: x
inteiro: a

inteiro func()
	retorna (x)
fim

inteiro principal()
	a := 10
	x:=15
	x:=a
	
retorna(a)
fim
