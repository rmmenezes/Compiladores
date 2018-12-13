; ModuleID = "gencode-005.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"soma"() 
{
soma.start:
  %"return" = alloca i32
}

define i32 @"main"() 
{
main.start:
  %"return" = alloca i32
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"retorna" = load i32, i32* %"return", align 4
  %"retorna.1" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  store i32 0, i32* %"return"
  %"ret" = load i32, i32* %"return"
  ret i32 %"ret"
}
