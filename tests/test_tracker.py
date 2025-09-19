from datetime import datetime
from pathlib import Path

import json

import pytest

from finance_app.tracker import FinanceTracker


def test_add_and_list_transactions(tmp_path: Path) -> None:
    storage = tmp_path / "dados.json"
    tracker = FinanceTracker(storage)

    tracker.add_transaction("entrada", "Salário", 2500.0, datetime(2023, 1, 10, 9, 0))
    tracker.add_transaction("saida", "Aluguel", 1200.0, datetime(2023, 1, 12, 10, 0))

    transactions = tracker.list_transactions()
    assert len(transactions) == 2
    assert transactions[0].description == "Salário"
    assert transactions[0].kind == "entrada"
    assert transactions[1].kind == "saida"

    saved = json.loads(storage.read_text(encoding="utf-8"))
    assert saved[0]["description"] == "Salário"
    assert saved[1]["value"] == 1200.0


def test_summary_returns_expected_values(tmp_path: Path) -> None:
    storage = tmp_path / "dados.json"
    tracker = FinanceTracker(storage)
    tracker.add_transaction("entrada", "Freelancer", 800.0, datetime(2023, 2, 1, 14, 30))
    tracker.add_transaction("saida", "Mercado", 200.0, datetime(2023, 2, 2, 18, 45))
    tracker.add_transaction("saida", "Transporte", 150.0, datetime(2023, 2, 3, 8, 15))

    resumo = tracker.get_summary()
    assert resumo["entradas"] == pytest.approx(800.0)
    assert resumo["saidas"] == pytest.approx(350.0)
    assert resumo["saldo"] == pytest.approx(450.0)


def test_invalid_transactions_raise_errors(tmp_path: Path) -> None:
    tracker = FinanceTracker(tmp_path / "dados.json")
    with pytest.raises(ValueError):
        tracker.add_transaction("bonus", "Inválido", 100.0)
    with pytest.raises(ValueError):
        tracker.add_transaction("entrada", "Negativo", -10)
