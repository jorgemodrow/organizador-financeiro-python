import csv
from datetime import datetime
import sqlite3

BANCO = "financas_pessoais.db"

CATEGORIAS_PADRAO = [
    ("Salário", "RECEITA"),
    ("Freelance / Extra", "RECEITA"),
    ("Alimentação", "DESPESA"),
    ("Transporte", "DESPESA"),
    ("Moradia", "DESPESA"),
    ("Saúde", "DESPESA"),
    ("Educação", "DESPESA"),
    ("Lazer", "DESPESA"),
    ("Outros", "DESPESA"),
]


def conectar():
    conn = sqlite3.connect(BANCO)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def inicializar_banco():
    with conectar() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('RECEITA', 'DESPESA'))
            );

            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor > 0),
                data_registro TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            );

            CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data_registro);
            CREATE INDEX IF NOT EXISTS idx_transacoes_cat ON transacoes(categoria_id);
            """
        )

        total_cat = conn.execute("SELECT COUNT(*) FROM categorias;").fetchone()[0]

        if total_cat == 0:
            conn.executemany(
                "INSERT INTO categorias (nome, tipo) VALUES (?, ?);",
                CATEGORIAS_PADRAO,
            )


def obter_categorias(tipo=None):
    with conectar() as conn:
        if tipo:
            return conn.execute(
                "SELECT id, nome FROM categorias WHERE tipo = ? ORDER BY id ASC;",
                (tipo,),
            ).fetchall()
        return conn.execute(
            "SELECT id, nome, tipo FROM categorias ORDER BY id ASC;"
        ).fetchall()


def cadastrar_categoria(nome, tipo):
    nome_formatado = nome.strip()
    if not nome_formatado:
        return False, "Nome inválido."

    with conectar() as conn:
        try:
            conn.execute(
                "INSERT INTO categorias (nome, tipo) VALUES (?, ?);",
                (nome_formatado, tipo.upper()),
            )
            return True, f"Categoria '{nome_formatado}' cadastrada com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Essa categoria já existe ou o tipo é inválido."


def registrar_transacao(descricao, valor, categoria_id, data_registro=None):
    if not descricao.strip():
        return False, "A descrição não pode ser vazia."
    if valor <= 0:
        return False, "O valor precisa ser maior que zero."

    # Se nao mandar data, pega a de hoje no formato YYYY-MM-DD
    if not data_registro:
        data_registro = datetime.now().strftime("%Y-%m-%d")

    with conectar() as conn:
        cat = conn.execute(
            "SELECT id FROM categorias WHERE id = ?;", (categoria_id,)
        ).fetchone()
        if not cat:
            return False, "Categoria inexistente."

        conn.execute(
            """
            INSERT INTO transacoes (descricao, valor, data_registro, categoria_id)
            VALUES (?, ?, ?, ?);
            """,
            (descricao.strip(), valor, data_registro, categoria_id),
        )
        return True, "Transação registrada com sucesso!"


def excluir_transacao(transacao_id):
    """Exclui uma transação pelo ID após validar se existe."""
    with conectar() as conn:
        transacao = conn.execute(
            "SELECT id, descricao, valor FROM transacoes WHERE id = ?;",
            (transacao_id,),
        ).fetchone()

        if not transacao:
            return False, "Transação não encontrada."

        conn.execute(
            "DELETE FROM transacoes WHERE id = ?;",
            (transacao_id,),
        )
        return (
            True,
            f"Transação #{transacao[0]} ('{transacao[1]}') excluída com sucesso!",
        )


def obter_fechamento_mensal(mes_ano=None):
    if not mes_ano:
        mes_ano = datetime.now().strftime("%Y-%m")

    query = """
        SELECT
            COALESCE(SUM(CASE WHEN c.tipo = 'RECEITA' THEN t.valor ELSE 0 END), 0) AS total_receitas,
            COALESCE(SUM(CASE WHEN c.tipo = 'DESPESA' THEN t.valor ELSE 0 END), 0) AS total_despesas
        FROM transacoes t
        JOIN categorias c ON t.categoria_id = c.id
        WHERE strftime('%Y-%m', t.data_registro) = ?;
    """
    with conectar() as conn:
        res = conn.execute(query, (mes_ano,)).fetchone()
        receitas, despesas = res[0], res[1]
        saldo = receitas - despesas
        return receitas, despesas, saldo, mes_ano


def obter_gastos_por_categoria(mes_ano=None):
    if not mes_ano:
        mes_ano = datetime.now().strftime("%Y-%m")

    query = """
        SELECT c.nome, SUM(t.valor) AS total_gasto
        FROM transacoes t
        JOIN categorias c ON t.categoria_id = c.id
        WHERE c.tipo = 'DESPESA' AND strftime('%Y-%m', t.data_registro) = ?
        GROUP BY c.id, c.nome
        ORDER BY total_gasto DESC;
    """
    with conectar() as conn:
        return conn.execute(query, (mes_ano,)).fetchall()

def obter_gastos_do_mes(mes_ano=None):
    if not mes_ano:
        mes_ano = datetime.now().strftime("%Y-%m")

    query = """
        SELECT t.data_registro, t.descricao, c.nome, t.valor FROM transacoes t
        JOIN categorias c ON t.categoria_id = c.id
        WHERE c.tipo = 'DESPESA' AND strftime('%Y-%m', t.data_registro) = ?
        ORDER BY t.data_registro ASC;
    """
    with conectar() as conn:
        return conn.execute(query, (mes_ano,)).fetchall()


def obter_historico_recente(limite=15):
    query = """
        SELECT t.id, t.data_registro, t.descricao, c.nome, c.tipo, t.valor
        FROM transacoes t
        JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.data_registro DESC, t.id DESC
        LIMIT ?;
    """
    with conectar() as conn:
        return conn.execute(query, (limite,)).fetchall()


def exportar_para_csv(nome_arquivo="extrato_financeiro.csv"):
    query = """
        SELECT t.id, t.data_registro, t.descricao, c.nome, c.tipo, t.valor
        FROM transacoes t
        JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.data_registro ASC;
    """
    try:
        with conectar() as conn:
            linhas = conn.execute(query).fetchall()

            if not linhas:
                return False, "Nenhuma transação cadastrada para exportar."

            with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arq:
                escritor = csv.writer(arq, delimiter=",")
                escritor.writerow(["ID", "Data", "Descrição", "Categoria", "Tipo", "Valor (R$)"])
                for lin in linhas:
                    escritor.writerow(lin)

            return True, f"Arquivo '{nome_arquivo}' gerado com sucesso!"
    except IOError as e:
        return False, f"Erro ao acessar arquivo: {e}"