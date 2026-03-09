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


def import_master_from_csv(user_id: str, lines: List[str]) -> int:
    """CSVからマスタカテゴリを一括インポート

    CSVフォーマット（ヘッダーなし）:
      タブ文字の数で階層を表現する。
      タブ0個 = 階層1（ルート）
      タブ1個 = 階層2
      タブ2個 = 階層3
      タブ3個 = 階層4
      ...

    例:
      科目A
      \tテクノロジ系
      \t\t基礎理論
      \t\t\t基礎理論
      \t\t\tアルゴリズムとプログラミング
      \t\tコンピュータ構成要素
      \t\t\tプロセッサ
      科目B
      ...
    """
    df = _read_master(user_id)

    # master_id スタック（深さ → master_id）
    # stack[i] = 深さiの直近のmaster_id
    id_stack: List[Optional[str]] = []

    new_rows = []

    # 既存データの name+parent_id セットで重複チェック
    existing_set = set()
    if df is not None:
        for _, row in df.iterrows():
            existing_set.add((row["name"], row["parent_id"] if pd.notna(row["parent_id"]) else ""))

    # 既存データのmaster_idも名前→IDで参照できるように
    # （同名が複数ある可能性があるため、ここでは使わずスタックで管理）

    for line in lines:
        # 空行スキップ
        if not line.strip():
            continue

        # タブ数を数えて深さを算出
        depth = 0
        for ch in line:
            if ch == "\t":
                depth += 1
            else:
                break

        name = line.strip()
        if not name:
            continue

        # 深さに合わせてスタックを調整
        # スタックを現在の深さに切り詰める
        id_stack = id_stack[:depth]

        # 親IDを取得（depth=0ならルート）
        parent_id = id_stack[depth - 1] if depth > 0 and len(id_stack) >= depth else ""

        # 重複チェック
        key = (name, parent_id)
        if key in existing_set:
            # 既存のIDをスタックに積む必要があるため取得
            if df is not None:
                matched = df[
                    (df["name"] == name) &
                    (df["parent_id"].fillna("") == parent_id)
                ]
                if not matched.empty:
                    existing_id = matched.iloc[0]["master_id"]
                    id_stack.append(existing_id)
                else:
                    id_stack.append(None)
            else:
                id_stack.append(None)
            continue

        new_master_id = str(uuid.uuid4())
        new_rows.append({
            "master_id": new_master_id,
            "name": name,
            "parent_id": parent_id,
        })
        existing_set.add(key)
        id_stack.append(new_master_id)

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True) if df is not None else new_df
        _write_master(user_id, df)

    return len(new_rows)
