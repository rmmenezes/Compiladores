; ModuleID = "gencode-002.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = common global i32 0, align 4
define i32 @"main"() 
{
main.start:
  %"return" = alloca i32
  %"ret" = alloca i32, align 4
  store i32 10, i32* @"a"
  %"varTempLeft" = load i32, i32* @"a"
  %"if_0" = icmp sgt i32 %"varTempLeft", 5
  br i1 %"if_0", label %"iftrue_0", label %"iffalse_0"
iftrue_0:
  store i32 1, i32* %"ret"
  br label %"ifend_0"
iffalse_0:
  store i32 5, i32* %"ret"
  br label %"ifend_0"
ifend_0:
  store i32 1, i32* %"ret"
  store i32 5, i32* %"ret"
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  %"varTemp" = load i32, i32* %"ret"
  store i32 %"varTemp", i32* %"return"
  %"ret.1" = load i32, i32* %"return"
  ret i32 %"ret.1"
}
