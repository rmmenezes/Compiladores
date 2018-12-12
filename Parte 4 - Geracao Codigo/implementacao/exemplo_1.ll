; ModuleID = "Exemplo_1"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"soma"(i32 %"a", i32 %"b") 
{
soma.start:
  %"retorna" = alloca i32
  %".4" = alloca i32, i32 a
  store i32 %"a", i32* %".4"
  %".6" = alloca i32, i32 b
  store i32 %"b", i32* %".6"
  %"result" = add i32* %".4", %".6"
  br label %"retorna.start"
soma.end:
  %".13" = load i32, i32* %"retorna"
  ret i32 %".13"
retorna.start:
  %".9" = load i32, i32* %"result"
  store i32 %".9", i32* %"retorna"
  br label %"soma.end"
retorna.fim:
  br label %"soma.end"
}

define void @"main"() 
{
main.start:
  %"a" = alloca i32
  %"b" = alloca i32
  %"retorno" = call i32 (...) @"scanf"([3 x i8]* @"0", i32* %"a")
  %"retorno.1" = call i32 (...) @"scanf"([3 x i8]* @"1", i32* %"b")
  %".2" = load i32, i32* %"a"
  %".3" = load i32, i32* %"b"
  %"retorno.2" = call i32 @"soma"(i32 %".2", i32 %".3")
  %"retorno.3" = call i32 (...) @"printf"([4 x i8]* @"2", i32 %"retorno.2")
  br label %"main.end"
main.end:
  ret void
}

declare i32 @"scanf"(...) 

@"0" = constant [3 x i8] c"%d\00"
@"1" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(...) 

@"2" = constant [4 x i8] c"%d\0a\00"