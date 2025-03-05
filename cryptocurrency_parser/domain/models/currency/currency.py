from dataclasses import dataclass
from datetime import datetime

from cryptocurrency_parser.domain.models.currency.currency_id import CurrencyId


@dataclass
class Currency:
    id: CurrencyId | None
    ticker: str
    full_name: str
    max_supply: int | None
    circulating_supply: int
    last_updated: datetime | None
