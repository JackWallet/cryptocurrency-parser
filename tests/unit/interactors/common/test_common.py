from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from unittest.mock import Mock

import pytest_asyncio
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)

from cryptocurrency_parser.application.price_history.price_history_gateway import (
    PriceHistoryAdder,
    PriceHistoryReader,
    PriceHistoryRemover,
)
from cryptocurrency_parser.domain.models.currency.currency_id import CurrencyId
from cryptocurrency_parser.domain.models.price_history.price_history import (
    PriceHistory,
)
from cryptocurrency_parser.domain.models.price_history.price_history_id import (
    PriceHistoryId,
)


class MockGatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_reader(self) -> PriceHistoryReader:
        return Mock()

    @provide
    def provide_adder(self) -> PriceHistoryAdder:
        return Mock()

    @provide
    def provide_remover(self) -> PriceHistoryRemover:
        return Mock()


@pytest_asyncio.fixture(scope="package")
async def container() -> AsyncGenerator[AsyncContainer, None]:
    container = make_async_container(MockGatewayProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture(scope="module")
def mock_valid_price_history() -> PriceHistory:
    return PriceHistory(
        id=PriceHistoryId(1),
        currency_id=CurrencyId(1),
        updated_at=datetime.now(tz=UTC),
        market_cap=Decimal(12),
        circulating_supply=1,
        market_cap_dominance=1,
        percent_change_1h=1,
        percent_change_24h=1,
        percent_change_30d=1,
        percent_change_60d=1,
        percent_change_7d=1,
        percent_change_90d=1,
        price=Decimal(1),
        volume_24h=Decimal(1),
    )


@pytest_asyncio.fixture(scope="package")
async def reader_valid(
    container: AsyncContainer,
    mock_valid_price_history: PriceHistory,
) -> Any:  # noqa: ANN401
    reader = await container.get(PriceHistoryReader)
    reader.get_by_id = Mock(return_value=mock_valid_price_history)
    reader.get_by_currency_id = Mock(return_value=[mock_valid_price_history])
    reader.get_by_currency_ids = Mock(return_value=[mock_valid_price_history])
    reader.get_highest_recorded_price_by_currency_id = Mock(
        return_value=mock_valid_price_history,
    )
    reader.get_last_record = Mock(return_value=mock_valid_price_history)
    return reader


@pytest_asyncio.fixture(scope="package")
async def adder(container: AsyncContainer) -> Any:  # noqa: ANN401
    return await container.get(PriceHistoryAdder)


@pytest_asyncio.fixture(scope="package")
async def remover(container: AsyncContainer) -> Any:  # noqa: ANN401
    return await container.get(PriceHistoryRemover)
