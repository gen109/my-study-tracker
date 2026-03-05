import uuid
import pandas as pd
from typing import List, Optional
from app.models.category import Category, CategoryCreate
from app.services.csv_service import read_csv, write_csv

FILENAME = "categories.csv"


def create_category(user_id: str, category: CategoryCreate) -> Category:
    """カテゴリを新規登録する"""
    df = read_csv(user_id, category.exam_id, FILENAME)

    new_row = {
        "category_id": str(uuid.uuid4()),
        "name": category.name,
        "exam_id": category.exam_id,
        "parent_id": category.parent_id if category.parent_id else "",
    }

    if df is None:
        df = pd.DataFrame([new_row])
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    write_csv(user_id, category.exam_id, FILENAME, df)
    return Category(**{**new_row, "children": []})


def get_categories(user_id: str, exam_id: str) -> List[Category]:
    """試験に紐づく全カテゴリを階層構造で返す"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return []

    # 全カテゴリをフラットなリストとして取得
    all_categories = {
        row["category_id"]: Category(
            category_id=row["category_id"],
            name=row["name"],
            exam_id=row["exam_id"],
            parent_id=row["parent_id"] if row["parent_id"] else None,
            children=[],
        )
        for _, row in df.iterrows()
    }

    # 階層構造を組み立て
    roots = []
    for category in all_categories.values():
        if category.parent_id and category.parent_id in all_categories:
            all_categories[category.parent_id].children.append(category)
        else:
            roots.append(category)

    return roots
