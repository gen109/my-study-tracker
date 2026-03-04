from pydantic import BaseModel
from typing import Optional
from datetime import date


class ExamBase(BaseModel):
    name: str                          # 試験名称（例：基本情報技術者試験）
    exam_date: Optional[date] = None   # 試験日
    has_range: bool = False            # 出題範囲設定（あり・なし）


class ExamCreate(ExamBase):
    pass


class Exam(ExamBase):
    exam_id: str                       # 試験ID（自動生成）

    class Config:
        from_attributes = True
