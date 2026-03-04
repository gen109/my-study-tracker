from pydantic import BaseModel
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str                              # カテゴリ名
    exam_id: str                           # 所属する試験ID
    parent_id: Optional[str] = None        # 親カテゴリID（Noneの場合はルート）


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    category_id: str                       # カテゴリID（自動生成）
    children: List["Category"] = []        # 子カテゴリ（再帰構造）

    class Config:
        from_attributes = True


# 再帰構造の解決
Category.model_rebuild()
