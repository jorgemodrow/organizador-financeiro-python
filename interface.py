from datetime import datetime


def linha(tamanho=65):
    return "-" * tamanho


def cabecalho(texto, tamanho=65):
    print("=" * tamanho)
    print(texto.center(tamanho))
    print("=" * tamanho)


def leia_int(msg):
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("\033[31mERRO: digite um número inteiro válido.\033[m")
        except KeyboardInterrupt:
            print("\n\033[31mEntrada cancelada.\033[m")
            return 0


def leia_float(msg):
    while True:
        try:
            entrada = input(msg).strip().replace(",", ".")
            valor = float(entrada)
            if valor <= 0:
                print("\033[31mERRO: o valor deve ser maior que zero.\033[m")
                continue
            return valor
        except ValueError:
            print(
                "\033[31mERRO: digite um valor monetário válido (ex: 25.50).\033[m"
            )
        except KeyboardInterrupt:
            print("\n\033[31mEntrada cancelada.\033[m")
            return 0.0


def leia_data_opcional(msg):
    """Lê data em AAAA-MM-DD ou retorna hoje se der enter vazio."""
    while True:
        try:
            entrada = input(msg).strip()
            if not entrada:
                return datetime.now().strftime("%Y-%m-%d")
            # Valida formato AAAA-MM-DD
            data_valida = datetime.strptime(entrada, "%Y-%m-%d")
            return data_valida.strftime("%Y-%m-%d")
        except ValueError:
            print("\033[31mERRO: formato inválido! Use AAAA-MM-DD (ex: 2026-09-15).\033[m")
        except KeyboardInterrupt:
            print("\n\033[31mEntrada cancelada.\033[m")
            return None


def leia_mes_ano_opcional(msg):
    """Lê AAAA-MM ou retorna mês atual se vazio."""
    while True:
        try:
            entrada = input(msg).strip()
            if not entrada:
                return datetime.now().strftime("%Y-%m")
            datetime.strptime(entrada, "%Y-%m")
            return entrada
        except ValueError:
            print("\033[31mERRO: formato inválido! Use AAAA-MM (ex: 2026-08).\033[m")
        except KeyboardInterrupt:
            print("\n\033[31mEntrada cancelada.\033[m")
            return None


def msg_sucesso(texto):
    print(f"\033[32m{texto}\033[m")


def msg_erro(texto):
    print(f"\033[31m{texto}\033[m")


def msg_alerta(texto):
    print(f"\033[33m{texto}\033[m")