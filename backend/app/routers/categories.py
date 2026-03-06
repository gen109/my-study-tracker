from fastapi import APIRouter
from typing import List
from app.models.category import Category, CategoryCreate
from app.services.category_service import create_category, get_categories

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=Category)
def add_category(user_id: str, category: CategoryCreate):
    """カテゴリを新規登録する"""
    return create_category(user_id, category)


@router.get("/{exam_id}", response_model=List[Category])
def list_categories(user_id: str, exam_id: str):
    """試験に紐づくカテゴリを階層構造で取得する"""
    return get_categories(user_id, exam_id)
