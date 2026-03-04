from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScoreBase(BaseModel):
    exam_id: str                           # 試験ID
    category_id: str                       # カテゴリID
    score: float                           # スコア（点数）
    max_score: float                       # 満点
    note: Optional[str] = None             # メモ（任意）


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    score_id: str                          # スコアID（自動生成）
    recorded_at: datetime                  # 記録日時（自動設定）

    class Config:
        from_attributes = True


class ScoreComparison(BaseModel):
    category_id: str
    category_name: str
    initial: Optional[float] = None        # 初回スコア
    previous: Optional[float] = None       # 前回スコア
    latest: Optional[float] = None         # 最新スコア
