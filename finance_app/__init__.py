"""Aplicativo simples de finanças pessoais.

Este pacote oferece utilidades para registrar transações de entrada e
saída de recursos de maneira persistente e uma interface de linha de
comando para interagir com os dados.
"""

from .tracker import FinanceTracker, Transaction

__all__ = ["FinanceTracker", "Transaction"]
