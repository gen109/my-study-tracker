from fastapi import APIRouter, HTTPException
from typing import List
from app.models.score import Score, ScoreCreate, ScoreComparison, ScoreUpdate
from app.services.score_service import (
    create_score,
    update_score,
    delete_score,
    get_scores_by_category,
    get_score_comparison,
)
from app.services.category_service import get_categories

router = APIRouter(prefix="/scores", tags=["scores"])


@router.post("/", response_model=Score)
def add_score(user_id: str, score: ScoreCreate):
    """スコアを蓄積型で登録する"""
    return create_score(user_id, score)


@router.put("/{exam_id}/{score_id}", response_model=Score)
def edit_score(exam_id: str, score_id: str, user_id: str, body: ScoreUpdate):
    """スコアを編集する"""
    result = update_score(user_id, exam_id, score_id, body.score, body.max_score, body.note)
    if result is None:
        raise HTTPException(status_code=404, detail="スコアが見つかりません")
    return result


@router.delete("/{exam_id}/{score_id}")
def remove_score(exam_id: str, score_id: str, user_id: str):
    """スコアを削除する"""
    success = delete_score(user_id, exam_id, score_id)
    if not success:
        raise HTTPException(status_code=404, detail="スコアが見つかりません")
    return {"message": "削除しました"}


@router.get("/{exam_id}/history", response_model=List[Score])
def score_history(exam_id: str, user_id: str, category_id: str):
    """カテゴリ別のスコア全履歴を返す"""
    return get_scores_by_category(user_id, exam_id, category_id)


@router.get("/{exam_id}/comparison", response_model=List[ScoreComparison])
def score_comparison(user_id: str, exam_id: str):
    """カテゴリ別の初回・前回・最新スコアを返す"""
    comparisons = get_score_comparison(user_id, exam_id)

    # カテゴリ名を付与
    categories = get_categories(user_id, exam_id)
    category_map = {}

    def flatten(nodes):
        for node in nodes:
            category_map[node.category_id] = node.name
            if node.children:
                flatten(node.children)

    flatten(categories)

    for c in comparisons:
        c.category_name = category_map.get(c.category_id, c.category_id)

    return comparisons
