import uuid
import pandas as pd
from datetime import datetime
from typing import List, Optional
from app.models.score import Score, ScoreCreate, ScoreComparison
from app.services.csv_service import read_csv, append_csv, write_csv

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


def update_score(user_id: str, exam_id: str, score_id: str, score: float, max_score: float, note: Optional[str] = None) -> Optional[Score]:
    """スコアを編集する"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return None

    idx = df[df["score_id"] == score_id].index
    if idx.empty:
        return None

    df.loc[idx, "score"] = score
    df.loc[idx, "max_score"] = max_score
    df.loc[idx, "note"] = note if note else ""
    write_csv(user_id, exam_id, FILENAME, df)

    row = df.loc[idx[0]]
    return Score(
        score_id=str(row["score_id"]),
        exam_id=str(row["exam_id"]),
        category_id=str(row["category_id"]),
        score=float(row["score"]),
        max_score=float(row["max_score"]),
        note=str(row["note"]) if pd.notna(row["note"]) else "",
        recorded_at=row["recorded_at"],
    )


def delete_score(user_id: str, exam_id: str, score_id: str) -> bool:
    """スコアを削除する"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return False

    new_df = df[df["score_id"] != score_id]
    if len(new_df) == len(df):
        return False

    write_csv(user_id, exam_id, FILENAME, new_df)
    return True


def get_scores_by_category(user_id: str, exam_id: str, category_id: str) -> List[Score]:
    """カテゴリ別の全スコア履歴を返す"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return []

    df = df[df["category_id"] == category_id].sort_values("recorded_at")
    return [
        Score(
            score_id=str(row["score_id"]),
            exam_id=str(row["exam_id"]),
            category_id=str(row["category_id"]),
            score=float(row["score"]),
            max_score=float(row["max_score"]),
            note=str(row["note"]) if pd.notna(row["note"]) else "",
            recorded_at=row["recorded_at"],
        )
        for _, row in df.iterrows()
    ]


def get_score_comparison(user_id: str, exam_id: str) -> List[ScoreComparison]:
    """カテゴリ別に初回・前回・最新スコアを返す"""
    df = read_csv(user_id, exam_id, FILENAME)
    if df is None:
        return []

    df = df.sort_values("recorded_at")

    results = []
    for category_id, group in df.groupby("category_id"):
        rates = [
            round(row["score"] / row["max_score"] * 100, 1)
            if row["max_score"] > 0 else 0
            for _, row in group.iterrows()
        ]

        initial = rates[0] if len(rates) >= 1 else None
        previous = rates[-2] if len(rates) >= 2 else None
        latest = rates[-1] if len(rates) >= 1 else None

        results.append(ScoreComparison(
            category_id=str(category_id),
            category_name=str(category_id),
            initial=initial,
            previous=previous,
            latest=latest,
        ))

    return results
