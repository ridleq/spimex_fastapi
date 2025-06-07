import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from models import TradeResult


@pytest.fixture
def trade_result_obj():
    return TradeResult(
        id=1,
        exchange_product_id="P-1",
        exchange_product_name="Product One",
        oil_id="OIL-1",
        delivery_basis_id="BASIS-1",
        delivery_basis_name="Basis Name",
        delivery_type_id="TYPE-1",
        volume=100.5,
        total=5050,
        count=3,
        date=datetime(2024, 6, 10),
        created_on=datetime(2024, 6, 9),
        updated_on=datetime(2024, 6, 9),
    )


@pytest.fixture
def trade_result_list(trade_result_obj):
    return [trade_result_obj]


@pytest.fixture
def session_mock(trade_result_list):
    mock = AsyncMock()
    exec_result = MagicMock()
    exec_result.scalars.return_value.all.return_value = trade_result_list
    exec_result.fetchall.return_value = [
        (tr.date,) for tr in trade_result_list
    ]
    mock.execute.return_value = exec_result
    return mock
