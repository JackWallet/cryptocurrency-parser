from dataclasses import dataclass

from cryptocurrency_parser.application.common.interactor import Interactor
from cryptocurrency_parser.application.price_history.price_history_gateway import (
    PriceHistoryReader,
)
from cryptocurrency_parser.domain.models.price_history.price_history import (
    PriceHistory,
)


@dataclass(frozen=True)
class GetHighestRecordedPriceDTO:
    full_name: str


class GetHighestRecordedPrice(
    Interactor[GetHighestRecordedPriceDTO, PriceHistory],
):
    def __init__(
        self,
        price_history_db_gateway: PriceHistoryReader,
    ) -> None:
        self._price_history_db_gateway = price_history_db_gateway

    async def __call__(self, data: GetHighestRecordedPriceDTO) -> PriceHistory:
        return await self._price_history_db_gateway.get_highest_recorded_price(
            currency_full_name=data.full_name,
        )
