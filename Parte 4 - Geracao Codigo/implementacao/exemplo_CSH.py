from llvmlite import ir


def declara_local_var(builder, tipo, name):
    return builder.alloca(tipo, name=name)


def declara_funcao_externa(module, name):
    func_type = ir.FunctionType(ir.IntType(32), (), var_arg=True)
    return module.declare_intrinsic(name, (), func_type)


def chama_funcao(builder, funcao, args):
    return builder.call(funcao, args, 'retorno')


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


def declaracao_funcao_main(modulo, name, funcao_soma, tipo_retorno_funcao=ir.VoidType()):
    # Declarando função
    tipo_funcao = ir.FunctionType(tipo_retorno_funcao, [])
    funcao_declarada = ir.Function(modulo, tipo_funcao, name=name)

    bloco_inicio = funcao_declarada.append_basic_block('%s.start' % name)
    bloco_fim = funcao_declarada.append_basic_block('%s.end' % name)

    builder = ir.IRBuilder(bloco_inicio)

    # Entrando na função funcao_declarada
    with builder.goto_entry_block():
        # inteiro: a, b
        a = declara_local_var(builder, ir.IntType(32), 'a')
        b = declara_local_var(builder, ir.IntType(32), 'b')

        # leia(a)
        leia = declara_funcao_externa(modulo, 'scanf')
        args = [declara_string_global(modulo, '%d\0'), a]
        chama_funcao(builder, leia, args)

        # leia(b)
        leia = declara_funcao_externa(modulo, 'scanf')
        args = [declara_string_global(modulo, '%d\0'), b]
        chama_funcao(builder, leia, args)

        # escreva(soma(a,b))
        args = [builder.load(a), builder.load(b)]
        res = chama_funcao(builder, funcao_soma, args)

        escreva = declara_funcao_externa(modulo, 'printf')
        args = [declara_string_global(modulo, '%d\n\0'), res]
        chama_funcao(builder, escreva, args)

        # Vai para o final da função
        builder.branch(bloco_fim)

    # Finaliza a função funcao_declarada
    with builder.goto_block(bloco_fim):
        builder.ret_void()

    return funcao_declarada


def declaracao_funcao_soma(modulo, name, tipo_retorno_funcao=ir.VoidType()):
    # Declarando função
    tipo_funcao = ir.FunctionType(tipo_retorno_funcao, [ir.IntType(32), ir.IntType(32)])
    funcao_declarada = ir.Function(modulo, tipo_funcao, name=name)

    bloco_inicio = funcao_declarada.append_basic_block('%s.start' % name)
    bloco_fim = funcao_declarada.append_basic_block('%s.end' % name)

    builder = ir.IRBuilder(bloco_inicio)

    # Deixa nomeado o parametro, não é realmente necessario fazer isso
    for arg, arg_name in zip(funcao_declarada.args, ['a', 'b']):
        arg.name = arg_name

    # Entrando na função funcao_declarada
    with builder.goto_entry_block():
        # Declara uma variavel para armazenar o retorno
        retorna = declara_local_var(builder, tipo_retorno_funcao, 'retorna')
        # (inteiro: a, inteiro: b)
        parametros = []
        for arg in funcao_declarada.args:
            param = builder.alloca(arg.type, arg.name)
            builder.store(arg, param)
            parametros.append(param)

        a = parametros[0]
        b = parametros[1]

        result = builder.add(a, b, 'result')

        chama_retorna(builder, retorna, result, bloco_fim, funcao_declarada)

        # Vai para o final da função
        builder.branch(bloco_fim)

    # Finaliza a função funcao_declarada
    with builder.goto_block(bloco_fim):
        retorna = builder.load(retorna)
        builder.ret(retorna)
    return funcao_declarada


if __name__ == '__main__':
    modulo = ir.Module('Exemplo_1')
    # renomeando principal para main
    """
        inteiro soma(inteiro: a, inteiro: b)
            retorna(a + b)
        fim
    """
    soma = declaracao_funcao_soma(modulo, 'soma', ir.IntType(32))
    """
    principal()
        inteiro: a, b
        leia(a)
        leia(b)
        escreva(soma(a,b))
    fim
    """
    main = declaracao_funcao_main(modulo, 'main', soma)

    with open('exemplo_1.ll', 'w') as f:
        f.write(str(modulo))
        print(modulo)
