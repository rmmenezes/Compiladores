; ModuleID = "gencode-001.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = common global i32 0, align 4
define i32 @"main"() 
{
main.start:
  %"return" = alloca i32
  %"b" = alloca i32, align 4
  store i32 10, i32* @"a"
  %"varTemp" = load i32, i32* @"a"
  store i32 %"varTemp", i32* %"b"
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  store i32 0, i32* %"return"
  %"ret" = load i32, i32* %"return"
  ret i32 %"ret"
}
