; ModuleID = "gencode-004.tpp"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"n" = common global i32 0, align 4
@"soma" = common global i32 0, align 4
define i32 @"main"() 
{
main.start:
  %"return" = alloca i32
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  %"varTempLeft" = load i32, i32* @"n"
  %"if_0" = icmp eq i32 %"varTempLeft", 0
  br label %"repitatrue_0"
repitatrue_0:
  %"varTempLeft.1" = load i32, i32* @"n"
  %"varTempLeft.2" = load i32, i32* @"soma"
  %"varTempAdd" = add i32 %"varTempLeft.2", %"varTempLeft.1"
  store i32 %"varTempAdd", i32* @"soma"
  %"varTempLeft.3" = load i32, i32* @"n"
  %"varTempSub" = sub i32 %"varTempLeft.3", 1
  store i32 %"varTempSub", i32* @"n"
  br i1 %"if_0", label %"repitaend_0", label %"repitatrue_0"
repitaend_0:
  %"varTempLeft.4" = load i32, i32* @"n"
  %"varTempLeft.5" = load i32, i32* @"soma"
  %"varTempAdd.1" = add i32 %"varTempLeft.5", %"varTempLeft.4"
  store i32 %"varTempAdd.1", i32* @"soma"
  %"varTempLeft.6" = load i32, i32* @"n"
  %"varTempSub.1" = sub i32 %"varTempLeft.6", 1
  store i32 %"varTempSub.1", i32* @"n"
  %"retorna" = load i32, i32* %"return", align 4
  br label %"main.end"
main.end:
  %"varTemp" = load i32, i32* @"soma"
  store i32 %"varTemp", i32* %"return"
  %"ret" = load i32, i32* %"return"
  ret i32 %"ret"
}
