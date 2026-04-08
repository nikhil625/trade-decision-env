from pydantic import BaseModel
from typing import List, Optional, Literal


class MarketState(BaseModel):
    price_history: List[float]
    rsi: float
    ema: float
    trend: str


class TradeProposal(BaseModel):
    action: Literal["BUY", "SELL"]
    stop_loss: float
    take_profit: float


class Observation(BaseModel):
    market: MarketState
    proposal: TradeProposal
    history: List[str]


class Action(BaseModel):
    decision: Literal["APPROVE", "REJECT", "MODIFY"]
    new_stop_loss: Optional[float] = None
    new_take_profit: Optional[float] = None


class Reward(BaseModel):
    value: float
    reason: str