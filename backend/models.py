from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class LotteryResult(SQLModel, table=True):
    """彩券開獎結果模型"""
    __tablename__ = "lottery_results"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    period: str = Field(index=True, unique=True)
    numbers: str  # 格式: "01, 05, 12, 23, 39"
    draw_date: str  # 格式: "2024-01-15"
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class Prediction(SQLModel, table=True):
    """預測記錄模型"""
    __tablename__ = "predictions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    period: str
    numbers: str
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


# API 回應模型
class LotteryResultResponse(SQLModel):
    """開獎結果回應"""
    id: int
    period: str
    numbers: str
    draw_date: str
    created_at: str


class PredictionResponse(SQLModel):
    """預測回應"""
    id: int
    period: str
    numbers: str
    created_at: str


class StatisticsResponse(SQLModel):
    """統計回應"""
    frequency: dict
    odd_even: dict
    ranges: dict


class ApiResponse(SQLModel):
    """通用 API 回應"""
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
