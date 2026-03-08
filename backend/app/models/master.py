from pydantic import BaseModel
from typing import Optional, List


class MasterCategoryBase(BaseModel):
    name: str                              # カテゴリ名
    parent_id: Optional[str] = None        # 親カテゴリID（Noneの場合はルート）


class MasterCategoryCreate(MasterCategoryBase):
    pass


class MasterCategory(MasterCategoryBase):
    master_id: str                         # マスタID（自動生成）
    children: List["MasterCategory"] = []  # 子カテゴリ（再帰構造）

    class Config:
        from_attributes = True


# 再帰構造の解決
MasterCategory.model_rebuild()
