import uuid
import pandas as pd
from typing import List, Optional
from app.models.master import MasterCategory, MasterCategoryCreate
from app.services.csv_service import DATA_ROOT

MASTER_FILENAME = "master_categories.csv"


def _get_master_path(user_id: str):
    path = DATA_ROOT / user_id / "master"
    path.mkdir(parents=True, exist_ok=True)
    return path / MASTER_FILENAME


def _read_master(user_id: str) -> Optional[pd.DataFrame]:
    path = _get_master_path(user_id)
    if not path.exists():
        return None
    df = pd.read_csv(path, dtype=str)
    return df if not df.empty else None


def _write_master(user_id: str, df: pd.DataFrame):
    path = _get_master_path(user_id)
    df.to_csv(path, index=False)


def create_master_category(user_id: str, category: MasterCategoryCreate) -> MasterCategory:
    """マスタカテゴリを新規登録（重複スキップ）"""
    df = _read_master(user_id)

    parent_id_val = category.parent_id if category.parent_id else ""
    if df is not None:
        duplicates = df[
            (df["name"] == category.name) &
            (df["parent_id"].fillna("") == parent_id_val)
        ]
        if not duplicates.empty:
            existing = duplicates.iloc[0]
            return MasterCategory(
                master_id=existing["master_id"],
                name=existing["name"],
                parent_id=existing["parent_id"] if pd.notna(existing["parent_id"]) and existing["parent_id"] else None,
                children=[],
            )

    new_row = {
        "master_id": str(uuid.uuid4()),
        "name": category.name,
        "parent_id": parent_id_val,
    }

    if df is None:
        df = pd.DataFrame([new_row])
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    _write_master(user_id, df)
    return MasterCategory(
        master_id=new_row["master_id"],
        name=new_row["name"],
        parent_id=category.parent_id,
        children=[],
    )


def get_master_categories(user_id: str) -> List[MasterCategory]:
    """マスタカテゴリを階層構造で返す"""
    df = _read_master(user_id)
    if df is None:
        return []

    all_categories = {
        row["master_id"]: MasterCategory(
            master_id=row["master_id"],
            name=row["name"],
            parent_id=row["parent_id"] if pd.notna(row["parent_id"]) and row["parent_id"] else None,
            children=[],
        )
        for _, row in df.iterrows()
    }

    roots = []
    for cat in all_categories.values():
        if cat.parent_id and cat.parent_id in all_categories:
            all_categories[cat.parent_id].children.append(cat)
        else:
            roots.append(cat)

    return roots


def delete_master_category(user_id: str, master_id: str) -> bool:
    """マスタカテゴリを削除（子も含めて削除）"""
    df = _read_master(user_id)
    if df is None:
        return False

    # 削除対象IDを再帰的に収集
    def collect_ids(target_id: str) -> set:
        ids = {target_id}
        children = df[df["parent_id"].fillna("") == target_id]["master_id"].tolist()
        for child_id in children:
            ids |= collect_ids(child_id)
        return ids

    ids_to_delete = collect_ids(master_id)
    new_df = df[~df["master_id"].isin(ids_to_delete)]
    _write_master(user_id, new_df)
    return True


def import_master_from_csv(user_id: str, rows: List[dict]) -> int:
    """CSVからマスタカテゴリを一括インポート
    CSVフォーマット: name, parent_name（親カテゴリ名。ルートの場合は空）
    """
    df = _read_master(user_id)

    # name → master_id のマッピング（既存 + 今回追加分）
    name_map: dict = {}
    if df is not None:
        for _, row in df.iterrows():
            name_map[row["name"]] = row["master_id"]

    new_rows = []
    for row in rows:
        name = str(row.get("name", "")).strip()
        parent_name = str(row.get("parent_name", "")).strip()
        if not name:
            continue

        parent_id = name_map.get(parent_name, "") if parent_name else ""

        # 重複チェック
        if df is not None:
            dup = df[
                (df["name"] == name) &
                (df["parent_id"].fillna("") == parent_id)
            ]
            if not dup.empty:
                name_map[name] = dup.iloc[0]["master_id"]
                continue

        new_master_id = str(uuid.uuid4())
        new_rows.append({
            "master_id": new_master_id,
            "name": name,
            "parent_id": parent_id,
        })
        name_map[name] = new_master_id

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True) if df is not None else new_df
        _write_master(user_id, df)

    return len(new_rows)
