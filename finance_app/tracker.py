"""Ferramentas para controlar transações financeiras simples.

O módulo define uma classe :class:`FinanceTracker` que gerencia
persistência em disco de transações representadas pela classe de dados
:class:`Transaction`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Iterable, List


@dataclass
class Transaction:
    """Representa uma transação financeira de entrada ou saída."""

    kind: str
    description: str
    value: float
    timestamp: str

    def to_dict(self) -> dict:
        """Converte a transação para um dicionário serializável."""

        return {
            "kind": self.kind,
            "description": self.description,
            "value": self.value,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Cria uma transação a partir de um dicionário."""

        return cls(
            kind=data["kind"],
            description=data["description"],
            value=float(data["value"]),
            timestamp=data["timestamp"],
        )


class FinanceTracker:
    """Gerencia uma coleção de transações em um arquivo JSON."""

    VALID_KINDS = {"entrada", "saida"}

    def __init__(self, storage_path: Path | str):
        self.storage_path = Path(storage_path)
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._write_transactions([])

    # ------------------------------------------------------------------
    # Operações internas de leitura e escrita
    def _read_transactions(self) -> List[Transaction]:
        if not self.storage_path.exists():
            return []
        try:
            raw_data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Arquivo de dados corrompido. Não foi possível interpretar o JSON."
            ) from exc
        return [Transaction.from_dict(item) for item in raw_data]

    def _write_transactions(self, transactions: Iterable[Transaction]) -> None:
        data = [t.to_dict() for t in transactions]
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # API pública
    def list_transactions(self) -> List[Transaction]:
        """Retorna todas as transações persistidas."""

        return self._read_transactions()

    def add_transaction(
        self,
        kind: str,
        description: str,
        value: float,
        timestamp: datetime | None = None,
    ) -> Transaction:
        """Adiciona uma transação de entrada ou saída.

        Args:
            kind: "entrada" para créditos ou "saida" para débitos.
            description: Descrição curta da transação.
            value: Valor positivo da transação.
            timestamp: Data e hora opcional. Se omitido é utilizado o momento
                atual.
        """

        normalized_kind = kind.lower().strip()
        if normalized_kind not in self.VALID_KINDS:
            raise ValueError(
                "Tipo de transação inválido. Utilize 'entrada' ou 'saida'."
            )
        if value <= 0:
            raise ValueError("O valor deve ser positivo.")

        moment = timestamp or datetime.now()
        transaction = Transaction(
            kind=normalized_kind,
            description=description.strip(),
            value=float(value),
            timestamp=moment.isoformat(timespec="seconds"),
        )

        transactions = self._read_transactions()
        transactions.append(transaction)
        self._write_transactions(transactions)
        return transaction

    def get_summary(self) -> dict:
        """Calcula totais de entrada, saída e saldo."""

        totals = {"entradas": 0.0, "saidas": 0.0}
        for transaction in self._read_transactions():
            if transaction.kind == "entrada":
                totals["entradas"] += transaction.value
            else:
                totals["saidas"] += transaction.value
        totals["saldo"] = totals["entradas"] - totals["saidas"]
        return totals

    def clear(self) -> None:
        """Remove todas as transações do arquivo de dados."""

        self._write_transactions([])
