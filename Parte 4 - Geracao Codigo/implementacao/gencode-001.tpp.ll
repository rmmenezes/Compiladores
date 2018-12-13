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
  %"varTemp" = load i32, i32* @"a", align 4
  store i32 %"varTemp", i32* %"b"
  br label %"main.end"
retorna.start:
  store i32 0, i32* %"return"
retorna.fim:
  %"b.1" = alloca i32, align 4
main.end:
}
