from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import io
import pandas as pd
from app.models.master import MasterCategory, MasterCategoryCreate
from app.services.master_service import (
    create_master_category,
    get_master_categories,
    delete_master_category,
    import_master_from_csv,
)

router = APIRouter(prefix="/masters", tags=["masters"])


@router.post("/", response_model=MasterCategory)
def add_master_category(user_id: str, category: MasterCategoryCreate):
    """マスタカテゴリを登録する"""
    return create_master_category(user_id, category)


@router.get("/", response_model=List[MasterCategory])
def list_master_categories(user_id: str):
    """マスタカテゴリ一覧を取得する"""
    return get_master_categories(user_id)


@router.delete("/{master_id}")
def remove_master_category(master_id: str, user_id: str):
    """マスタカテゴリを削除する（子も含めて削除）"""
    success = delete_master_category(user_id, master_id)
    if not success:
        raise HTTPException(status_code=404, detail="マスタカテゴリが見つかりません")
    return {"message": "削除しました"}


@router.post("/import-csv")
def import_csv(user_id: str, file: UploadFile = File(...)):
    """CSVからマスタカテゴリを一括インポートする
    CSVフォーマット（ヘッダー必須）:
      name, parent_name
    例:
      科目A,
      テクノロジ系,科目A
      基礎理論,テクノロジ系
    """
    content = file.file.read().decode("utf-8-sig")
    df = pd.read_csv(io.StringIO(content), dtype=str).fillna("")
    rows = df.to_dict(orient="records")
    count = import_master_from_csv(user_id, rows)
    return {"message": f"{count}件のカテゴリをインポートしました"}
