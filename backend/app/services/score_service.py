import uuid
import pandas as pd
from datetime import datetime
from typing import List
from app.models.score import Score, ScoreCreate, ScoreComparison
from app.services.csv_service import read_csv, append_csv

FILENAME = "scores.csv"


def create_score(user_id: str, score: ScoreCreate) -> Score:
    """スコアを蓄積型で追記保存する"""
    new_row = {
        "score_id": str(uuid.uuid4()),
        "exam_id": score.exam_id,
        "category_id": score.category_id,
        "score": score.score,
        "max_score": score.max_score,
        "note": score.note if score.note else "",
        "recorded_at": datetime.now().isoformat(),
    }

    append_csv(user_id, score.exam_id, FILENAME, pd.DataFrame([new_row]))
    return Score(**new_row)


def get_score_comparison(user_id: str, exam_id: str) -> List[ScoreComparison]:
    """カテゴリ別に初回・前回・最新スコアを返す"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return []

    # 記録日時で昇順ソート
    df = df.sort_values("recorded_at")

    results = []
    for category_id, group in df.groupby("category_id"):
        records = group["score"].tolist()

        initial = records[0] if len(records) >= 1 else None
        previous = records[-2] if len(records) >= 2 else None
        latest = records[-1] if len(records) >= 1 else None

        results.append(ScoreComparison(
            category_id=str(category_id),
            category_name=str(category_id),  # routers側でカテゴリ名を付与
            initial=initial,
            previous=previous,
            latest=latest,
        ))

    return results
