from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="my-study-tracker API",
    version="0.1.0",
)

# CORS設定（Vue.js開発サーバーからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録（後で追加）
from app.routers import exams, categories, scores
app.include_router(exams.router)
app.include_router(categories.router)
app.include_router(scores.router)

@app.get("/")
def root():
    return {"message": "my-study-tracker API is running"}