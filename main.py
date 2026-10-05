from datetime import datetime
import database as db
import interface as ui


def pausa():
    input("\nPressione <Enter> para voltar ao menu ")


def acao_lancar_transacao(tipo):
    titulo = ("NOVA DESPESA / GASTO" if tipo == "DESPESA" else "NOVA RECEITA / ENTRADA")
    ui.cabecalho(titulo)

    descricao = input("Descrição do lançamento: ").strip()
    if not descricao:
        ui.msg_erro("A descrição não pode ficar vazia.")
        pausa()
        return

    categorias = db.obter_categorias(tipo=tipo)
    print(f"\nCategorias de {tipo.lower()}:")
    for cat_id, nome in categorias:
        print(f"[{cat_id}] {nome}")

    cat_id = ui.leia_int("\nEscolha o número da categoria: ")
    ids_validos = [c[0] for c in categorias]

    if cat_id not in ids_validos:
        ui.msg_erro("Categoria selecionada inválida!")
        pausa()
        return

    valor = ui.leia_float("Valor (R$): ")
    if valor == 0:
        return

    data = ui.leia_data_opcional("Data (AAAA-MM-DD ou <Enter> para hoje): ")
    if data is None:
        return

    sucesso, msg = db.registrar_transacao(descricao, valor, cat_id, data)
    if sucesso:
        ui.msg_sucesso(
            f"{tipo.title()} de R$ {valor:.2f} registrada com sucesso em {data}!"
        )
    else:
        ui.msg_erro(msg)
    pausa()


def exibir_fechamento():
    ui.cabecalho("CONSULTA DE FECHAMENTO MENSAL")
    mes_filtro = ui.leia_mes_ano_opcional(
        "Mês de referência (AAAA-MM ou <Enter> para o mês atual): "
    )
    if not mes_filtro:
        return

    receitas, despesas, saldo, mes = db.obter_fechamento_mensal(mes_filtro)

    ui.cabecalho(f"FECHAMENTO MENSAL - [{mes}]")
    print(f"Total de Entradas (Receitas): R$ {receitas:>10.2f}")
    print(f"Total de Saídas   (Despesas): R$ {despesas:>10.2f}")

    cor_saldo = "\033[32m" if saldo >= 0 else "\033[31m"
    print(f"SALDO DO MÊS: {cor_saldo}R$ {saldo:>10.2f}\033[m")

    gastos_cat = db.obter_gastos_por_categoria(mes)
    if gastos_cat:
        ui.cabecalho(f"DISTRIBUIÇÃO DOS GASTOS")
        print(f"{'CATEGORIA':<25} {'TOTAL (R$)':<12} {'% DO MÊS'}")
        print(ui.linha())
        for cat_nome, total in gastos_cat:
            percentual = (total / despesas * 100) if despesas > 0 else 0
            print(f"{cat_nome:<25} R$ {total:>8.2f}    {percentual:>5.1f}%")
        print()
    else:
        ui.msg_alerta(f"Nenhuma despesa registrada para o período [{mes}].")

    gastos_mes = db.obter_gastos_do_mes(mes)
    if gastos_mes:
        ui.cabecalho("TODOS OS GASTOS")
        print(f"{'DATA':<11} {'DESCRIÇÃO':<22} {'CATEGORIA':<15} {'VALOR (R$)'}")
        print(ui.linha())
        for data, desc, cat, valor in gastos_mes:
            desc_formatada = desc if len(desc) <= 20 else f"{desc[:19]}.."
            print(f"{data:<11} {desc_formatada:<22} {cat:<15} R$ {valor:>8.2f}")
        print(ui.linha())

    pausa()

def exibir_extrato(pausar=True):
    ui.cabecalho("ÚLTIMOS LANÇAMENTOS REGISTRADOS")
    historico = db.obter_historico_recente(limite=15)

    if not historico:
        ui.msg_alerta("Nenhuma movimentação cadastrada.")
        if pausar:
            pausa()
        return False

    print(
        f"{'ID':<4} {'DATA':<11} {'DESCRIÇÃO':<20} {'CATEGORIA':<14} {'VALOR (R$)':>10}"
    )
    print(ui.linha())
    for tid, data, desc, cat, tipo, valor in historico:
        sinal = "+" if tipo == "RECEITA" else "-"
        cor = "\033[32m" if tipo == "RECEITA" else "\033[31m"
        desc_formatada = desc if len(desc) <= 18 else f"{desc[:17]}.."
        print(f"{tid:<4} {data:<11} {desc_formatada:<20} {cat:<14} {cor}{sinal} R$ {valor:>7.2f}\033[m")
    print(ui.linha())

    if pausar:
        pausa()
    return True


def acao_excluir_transacao():
    ui.cabecalho("EXCLUIR TRANSAÇÃO")
    tem_registros = exibir_extrato(pausar=False)

    if not tem_registros:
        pausa()
        return

    transacao_id = ui.leia_int(
        "\nInforme o ID da transação que deseja excluir (0 para cancelar): "
    )
    if transacao_id == 0:
        ui.msg_alerta("Operação cancelada.")
        pausa()
        return

    confirma = input(f"Tem certeza que deseja apagar a transação #{transacao_id}? (S/N): ").strip().upper()

    if confirma == "S":
        sucesso, msg = db.excluir_transacao(transacao_id)
        if sucesso:
            ui.msg_sucesso(msg)
        else:
            ui.msg_erro(msg)
    else:
        ui.msg_alerta("Exclusão cancelada.")

    pausa()


def acao_nova_categoria():
    ui.cabecalho("CRIAR NOVA CATEGORIA")
    nome = input("Nome da categoria: ").strip()
    if not nome:
        ui.msg_erro("O nome não pode ser vazio.")
        pausa()
        return

    print("\nTipo:")
    print("[1] Despesa")
    print("[2] Receita")
    opcao_tipo = ui.leia_int("Opção: ")

    tipo_map = {1: "DESPESA", 2: "RECEITA"}
    tipo = tipo_map.get(opcao_tipo)

    if not tipo:
        ui.msg_erro("Tipo inválido.")
        pausa()
        return

    sucesso, msg = db.cadastrar_categoria(nome, tipo)
    if sucesso:
        ui.msg_sucesso(msg)
    else:
        ui.msg_erro(msg)
    pausa()


def acao_exportar():
    ui.cabecalho("EXPORTAR EXTRATO PARA CSV")
    sucesso, msg = db.exportar_para_csv("extrato_financeiro.csv")
    if sucesso:
        ui.msg_sucesso(msg)
    else:
        ui.msg_erro(msg)
    pausa()


def exibir_menu():
    ui.cabecalho("ORGANIZADOR FINANCEIRO PESSOAL")
    print("1 - Lançar Novo Gasto / Despesa")
    print("2 - Lançar Nova Receita / Ganho")
    print("3 - Ver Fechamento Mensal")
    print("4 - Ver Últimos Lançamentos (Extrato)")
    print("5 - Excluir Transação")
    print("6 - Cadastrar Categoria Personalizada")
    print("7 - Exportar Dados para CSV (Excel / BI)")
    print("8 - Sair")
    print(ui.linha())


def menu():
    db.inicializar_banco()

    opcoes = {
        1: lambda: acao_lancar_transacao("DESPESA"),
        2: lambda: acao_lancar_transacao("RECEITA"),
        3: exibir_fechamento,
        4: exibir_extrato,
        5: acao_excluir_transacao,
        6: acao_nova_categoria,
        7: acao_exportar,
    }

    while True:
        exibir_menu()
        opcao = ui.leia_int("Sua opção: ")

        if opcao == 8:
            ui.msg_alerta("Encerrando o organizador financeiro... Valeu!")
            break

        funcao = opcoes.get(opcao)
        if funcao:
            funcao()
        else:
            ui.msg_erro("Opção inválida! Escolha entre 1 e 8.")
            pausa()


if __name__ == "__main__":
    menu()