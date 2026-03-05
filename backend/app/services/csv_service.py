import pandas as pd
from pathlib import Path
from typing import Optional

# データ保存先のルートパス
DATA_ROOT = Path(__file__).parent.parent.parent / "data"


def get_data_path(user_id: str, exam_id: str) -> Path:
    """ユーザー・試験ごとのデータフォルダパスを返す"""
    path = DATA_ROOT / user_id / exam_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_csv(user_id: str, exam_id: str, filename: str) -> Optional[pd.DataFrame]:
    """CSVファイルを読み込んでDataFrameで返す。ファイルが存在しない場合はNoneを返す"""
    filepath = get_data_path(user_id, exam_id) / filename
    if not filepath.exists():
        return None
    return pd.read_csv(filepath)


def write_csv(user_id: str, exam_id: str, filename: str, df: pd.DataFrame) -> None:
    """DataFrameをCSVファイルに書き込む（追記ではなく上書き）"""
    filepath = get_data_path(user_id, exam_id) / filename
    df.to_csv(filepath, index=False)


def append_csv(user_id: str, exam_id: str, filename: str, df: pd.DataFrame) -> None:
    """DataFrameをCSVファイルに追記する（履歴の蓄積）"""
    filepath = get_data_path(user_id, exam_id) / filename
    if filepath.exists():
        existing = pd.read_csv(filepath)
        combined = pd.concat([existing, df], ignore_index=True)
    else:
        combined = df
    combined.to_csv(filepath, index=False)
