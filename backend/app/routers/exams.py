import uuid
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.models.exam import Exam, ExamCreate
from app.services.csv_service import read_csv, write_csv

router = APIRouter(prefix="/exams", tags=["exams"])

FILENAME = "exams.csv"


@router.post("/", response_model=Exam)
def create_exam(user_id: str, exam: ExamCreate):
    """試験を新規登録する"""
    # user_idはパスではなくクエリパラメータで受け取る（認証実装前の暫定）
    new_row = {
        "exam_id": str(uuid.uuid4()),
        "name": exam.name,
        "exam_date": str(exam.exam_date) if exam.exam_date else "",
        "has_range": exam.has_range,
    }

    df = read_csv(user_id, new_row["exam_id"], FILENAME)
    if df is None:
        df = pd.DataFrame([new_row])
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    write_csv(user_id, new_row["exam_id"], FILENAME, df)
    return Exam(**new_row)


@router.get("/", response_model=list[Exam])
def get_exams(user_id: str):
    """試験一覧を取得する"""
    from pathlib import Path
    from app.services.csv_service import DATA_ROOT

    user_path = DATA_ROOT / user_id
    if not user_path.exists():
        return []

    exams = []
    for exam_dir in user_path.iterdir():
        if exam_dir.is_dir():
            df = read_csv(user_id, exam_dir.name, FILENAME)
            if df is not None:
                for _, row in df.iterrows():
                    exams.append(Exam(
                        exam_id=row["exam_id"],
                        name=row["name"],
                        exam_date=row["exam_date"] if row["exam_date"] else None,
                        has_range=row["has_range"],
                    ))
    return exams

@router.delete("/{exam_id}")
def delete_exam(exam_id: str, user_id: str):
    """試験を削除する"""
    from pathlib import Path
    from app.services.csv_service import DATA_ROOT
    import shutil

    exam_path = DATA_ROOT / user_id / exam_id
    if not exam_path.exists():
        raise HTTPException(status_code=404, detail="試験が見つかりません")

    shutil.rmtree(exam_path)
    return {"message": "削除しました"}
