inteiro: n
flutuante: x, y, z
n:=5
inteiro fatorial(inteiro: n, flutuante: m)
	m := 5.5
	
	se 0<6 então
		retorna(n)
	senão
		repita 
			flutuante: p
		até n = 0
	fim
	z := 1.9 {SEM ERRO, FOI INICIALIZADO}
	z := z+1 {ERRO, ID NAO FOI INICIALIZADO}
	retorna(m)
fim

inteiro principal()
    inteiro: x
    inteiro: y
    inteiro: res
    x:=1
    y:=2.2
    res:= x > y

    
fim