from fastapi import APIRouter
from typing import List
from app.models.score import Score, ScoreCreate, ScoreComparison
from app.services.score_service import create_score, get_score_comparison
from app.services.category_service import get_categories

router = APIRouter(prefix="/scores", tags=["scores"])


@router.post("/", response_model=Score)
def add_score(user_id: str, score: ScoreCreate):
    """スコアを蓄積型で登録する"""
    return create_score(user_id, score)


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
