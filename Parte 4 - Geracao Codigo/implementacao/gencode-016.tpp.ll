; ModuleID = "gencode-016.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
main.start:
  %"return" = alloca i32
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  store i32 0, i32* %"return"
  %"ret" = load i32, i32* %"return"
  ret i32 %"ret"
}
