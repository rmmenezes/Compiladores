; ModuleID = "gencode-005.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
main.start:
  %"return" = alloca i32
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"variavel" = load i32, i32* %"a"
  %".2" = call i32 (...) @"scanf"([4 x i8]* @"0", i32 %"variavel")
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  store i32 0, i32* %"return"
  %"ret" = load i32, i32* %"return"
  ret i32 %"ret"
}

declare i32 @"scanf"(...) 

@"0" = constant [4 x i8] c"%lf\00"