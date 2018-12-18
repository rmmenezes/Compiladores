; ModuleID = "Exemplo_1"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define double @"main"() 
{
main.start:
  %"a" = alloca double
  %"retorna" = alloca double
  %".2" = call i32 (...) @"scanf"([4 x i8]* @"0", double* %"a")
  %".3" = load double, double* %"a"
  %".4" = call i32 (...) @"printf"([5 x i8]* @"1", double %".3")
  br label %"retorna.start"
main.end:
  %".10" = load double, double* %"retorna"
  ret double %".10"
retorna.start:
  %".6" = load double, double* %"a"
  store double %".6", double* %"retorna"
  br label %"main.end"
retorna.fim:
  br label %"main.end"
}

declare i32 @"scanf"(...) 

@"0" = constant [4 x i8] c"%lf\00"
declare i32 @"printf"(...) 

@"1" = constant [5 x i8] c"%lf\0a\00"