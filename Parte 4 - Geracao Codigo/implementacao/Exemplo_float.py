from llvmlite import ir

"""
flutuante principal()
    flutuante: a
    leia(a)
    escreva(a)
    retorna(a)
fim
"""

def declara_local_var(builder, tipo, name):
    return builder.alloca(tipo, name=name)

def declara_funcao_externa(module, name):
    func_type = ir.FunctionType(ir.IntType(32), (), var_arg=True)
    return module.declare_intrinsic(name, (), func_type)

def chama_funcao(builder, funcao, args):
    builder.call(funcao, args)

global_string_name = 0

def declara_string_global(module, string_parametro):
    global global_string_name

    typ = ir.ArrayType(ir.IntType(8), len(string_parametro))
    # campo name deve ser unico
    tmp = ir.GlobalVariable(module, typ, name=str(global_string_name))
    global_string_name += 1

    tmp.initializer = ir.Constant(typ, bytearray(string_parametro, encoding='utf-8'))
    tmp.global_constant = True
    return tmp

def chama_retorna(builder, variavel_retorna, retorno_da_funcao, final_da_funcao, funcao_atual):
    inicio_retorna = funcao_atual.append_basic_block('retorna.start')

    builder.branch(inicio_retorna)
    with builder.goto_block(inicio_retorna):
        # Armazena o retorno da função
        retorna = builder.load(retorno_da_funcao)
        builder.store(retorna, variavel_retorna)
        # Vai para o final da função
        builder.branch(final_da_funcao)

    # positiona o ponteiro, utilizado caso o retorna não seja o ultimo comando
    fim_retorna = funcao_atual.append_basic_block('retorna.fim')
    builder.position_at_end(fim_retorna)

if __name__ == '__main__':
    modulo = ir.Module('Exemplo_1')
    # renomeando principal para main
    tipo_retorno_funcao = ir.DoubleType()

    # Declarando função
    tipo_funcao = ir.FunctionType(tipo_retorno_funcao, [])
    main = ir.Function(modulo, tipo_funcao, name='main')

    bloco_inicio_main = main.append_basic_block('main.start')
    bloco_fim_main = main.append_basic_block('main.end')

    builder = ir.IRBuilder(bloco_inicio_main)

    # Entrando na função main
    with builder.goto_entry_block():
        # flutuante: a
        a = declara_local_var(builder, ir.DoubleType(), 'a')

        # Declara uma variavel para armazenar o retorno
        retorna = declara_local_var(builder, tipo_retorno_funcao, 'retorna')

        # leia(a)
        leia = declara_funcao_externa(modulo, 'scanf')
        args = [declara_string_global(modulo, '%lf\0'), a]
        chama_funcao(builder, leia, args)

        # escreva(a)
        escreva = declara_funcao_externa(modulo, 'printf')
        args = [declara_string_global(modulo, '%lf\n\0'), builder.load(a)]
        chama_funcao(builder, escreva, args)

        # retorna(a)
        chama_retorna(builder, retorna, a, bloco_fim_main, main)

        # Vai para o final da função
        builder.branch(bloco_fim_main)

    # Finaliza a função main
    with builder.goto_block(bloco_fim_main):
        retorna = builder.load(retorna)
        builder.ret(retorna)

    
