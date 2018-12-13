; ModuleID = "gencode-003.tpp"
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
  %"varTempLeft.1" = load i32, i32* @"a"
  %"if_0.1" = icmp sgt i32 %"varTempLeft.1", 20
  br i1 %"if_0.1", label %"iftrue_0.1", label %"iffalse_0.1"
iffalse_0:
  store i32 0, i32* %"ret"
  br label %"ifend_0"
ifend_0:
  %"varTempLeft.2" = load i32, i32* @"a"
  %"if_2" = icmp sgt i32 %"varTempLeft.2", 20
  br i1 %"if_2", label %"iftrue_2", label %"iffalse_2"
iftrue_0.1:
  store i32 1, i32* %"ret"
  br label %"ifend_0.1"
iffalse_0.1:
  store i32 2, i32* %"ret"
  br label %"ifend_0.1"
ifend_0.1:
  store i32 1, i32* %"ret"
  store i32 2, i32* %"ret"
  br label %"ifend_0"
iftrue_2:
  store i32 1, i32* %"ret"
  br label %"ifend_2"
iffalse_2:
  store i32 2, i32* %"ret"
  br label %"ifend_2"
ifend_2:
  store i32 1, i32* %"ret"
  store i32 2, i32* %"ret"
  store i32 0, i32* %"ret"
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  store i32 0, i32* %"return"
  %"ret.1" = load i32, i32* %"return"
  ret i32 %"ret.1"
}
