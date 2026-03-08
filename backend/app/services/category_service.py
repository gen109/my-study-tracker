import uuid
import pandas as pd
from typing import List
from app.models.category import Category, CategoryCreate
from app.services.csv_service import read_csv, write_csv

FILENAME = "categories.csv"


def create_category(user_id: str, category: CategoryCreate) -> Category:
    """カテゴリを新規登録する（同名・同階層の重複はスキップしis_new=Falseを返す）"""
    df = read_csv(user_id, category.exam_id, FILENAME)

    # 重複チェック（同じ name かつ同じ parent_id が既に存在する場合はスキップ）
    if df is not None:
        parent_id_val = category.parent_id if category.parent_id else ""
        duplicates = df[
            (df["name"] == category.name) &
            (df["parent_id"].fillna("") == parent_id_val)
        ]
        if not duplicates.empty:
            existing = duplicates.iloc[0]
            result = Category(
                category_id=existing["category_id"],
                name=existing["name"],
                exam_id=existing["exam_id"],
                parent_id=existing["parent_id"] if pd.notna(existing["parent_id"]) and existing["parent_id"] else None,
                children=[],
            )
            result.is_new = False
            return result

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
    result = Category(**{**new_row, "children": []})
    result.is_new = True
    return result


def get_categories(user_id: str, exam_id: str) -> List[Category]:
    """試験に紐づく全カテゴリを階層構造で返す"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return []

    all_categories = {
        row["category_id"]: Category(
            category_id=row["category_id"],
            name=row["name"],
            exam_id=row["exam_id"],
            parent_id=row["parent_id"] if pd.notna(row["parent_id"]) and row["parent_id"] else None,
            children=[],
        )
        for _, row in df.iterrows()
    }

    roots = []
    for category in all_categories.values():
        if category.parent_id and category.parent_id in all_categories:
            all_categories[category.parent_id].children.append(category)
        else:
            roots.append(category)

    return roots
