from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
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

    CSVフォーマット（ヘッダーなし・タブで階層を表現）:
      タブ0個 = 階層1（ルート）
      タブ1個 = 階層2
      タブ2個 = 階層3
      タブ3個 = 階層4

    例:
      科目A
      [TAB]テクノロジ系
      [TAB][TAB]基礎理論
      [TAB][TAB][TAB]基礎理論
      [TAB][TAB][TAB]アルゴリズムとプログラミング
      科目B
    """
    content = file.file.read().decode("utf-8-sig")
    lines = content.splitlines()
    count = import_master_from_csv(user_id, lines)
    return {"message": f"{count}件のカテゴリをインポートしました"}
