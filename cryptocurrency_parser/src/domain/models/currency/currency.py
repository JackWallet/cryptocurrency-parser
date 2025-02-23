from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.models.currency.currency_id import CurrencyId

@dataclass
class Currency:
    id: Optional[CurrencyId]
    ticker: str
    full_name: str
    last_updated: datetime