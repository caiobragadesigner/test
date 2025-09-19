"""Interface de linha de comando para o aplicativo de finanças."""

from __future__ import annotations

import argparse
from pathlib import Path

from .tracker import FinanceTracker


DEFAULT_DATA_FILE = Path("dados_financeiros.json")


def format_currency(value: float) -> str:
    """Formata valores monetários utilizando separador brasileiro."""

    formatted = f"R$ {value:,.2f}"
    return formatted.replace(",", "_").replace(".", ",").replace("_", ".")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Controle simples de entradas e saídas financeiras.",
    )
    parser.add_argument(
        "--arquivo",
        default=str(DEFAULT_DATA_FILE),
        help="Caminho para o arquivo JSON onde as transações serão salvas.",
    )

    subparsers = parser.add_subparsers(dest="comando", required=True)

    adicionar = subparsers.add_parser(
        "adicionar", help="Registra uma nova transação de entrada ou saída."
    )
    adicionar.add_argument(
        "tipo",
        choices=sorted(FinanceTracker.VALID_KINDS),
        help="Tipo da transação: entrada ou saída de recursos.",
    )
    adicionar.add_argument(
        "descricao",
        help="Descrição breve da transação.",
    )
    adicionar.add_argument(
        "valor",
        type=float,
        help="Valor numérico da transação (use ponto como separador decimal).",
    )

    subparsers.add_parser("listar", help="Lista todas as transações registradas.")
    subparsers.add_parser(
        "resumo", help="Mostra o total de entradas, saídas e o saldo atual."
    )

    return parser


def handle_adicionar(args: argparse.Namespace, tracker: FinanceTracker) -> None:
    transaction = tracker.add_transaction(args.tipo, args.descricao, args.valor)
    sinal = "+" if transaction.kind == "entrada" else "-"
    print(
        "Transação adicionada:",
        f"{sinal}{format_currency(transaction.value)}",
        f"[{transaction.timestamp}]",
        transaction.description,
    )


def handle_listar(tracker: FinanceTracker) -> None:
    transactions = tracker.list_transactions()
    if not transactions:
        print("Nenhuma transação registrada até o momento.")
        return

    print("#  Data e hora           Tipo     Valor        Descrição")
    print("-" * 60)
    for idx, transaction in enumerate(transactions, start=1):
        tipo = "Entrada" if transaction.kind == "entrada" else "Saída  "
        valor = format_currency(transaction.value)
        print(
            f"{idx:>2} {transaction.timestamp:<19} {tipo:<8} {valor:<12} {transaction.description}",
        )


def handle_resumo(tracker: FinanceTracker) -> None:
    resumo = tracker.get_summary()
    print("Resumo financeiro")
    print("-" * 30)
    print("Entradas:", format_currency(resumo["entradas"]))
    print("Saídas:  ", format_currency(resumo["saidas"]))
    print("Saldo:   ", format_currency(resumo["saldo"]))


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    tracker = FinanceTracker(args.arquivo)

    if args.comando == "adicionar":
        handle_adicionar(args, tracker)
    elif args.comando == "listar":
        handle_listar(tracker)
    elif args.comando == "resumo":
        handle_resumo(tracker)
    else:  # pragma: no cover - proteção futura caso novos comandos sejam criados
        parser.error("Comando desconhecido")


if __name__ == "__main__":  # pragma: no cover
    main()
