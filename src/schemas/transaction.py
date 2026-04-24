from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DepositIn(BaseModel):
    amount: Decimal = Field(gt=0)


class WithdrawIn(BaseModel):
    amount: Decimal = Field(gt=0)


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
