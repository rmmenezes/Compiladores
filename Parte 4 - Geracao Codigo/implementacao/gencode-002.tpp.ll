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
  br i1 %"if_0", label %"iftrue", label %"iffalse"
iftrue:
  store i32 1, i32* %"ret"
  br label %"ifend"
iffalse:
  store i32 0, i32* %"ret"
  br label %"ifend"
ifend:
  store i32 1, i32* %"ret"
  store i32 0, i32* %"ret"
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  %"varTemp" = load i32, i32* %"ret"
  store i32 %"varTemp", i32* %"return"
  %"ret.1" = load i32, i32* %"return"
  ret i32 %"ret.1"
}
