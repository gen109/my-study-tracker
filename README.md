# 学習管理システム（my-study-tracker）

> 学習データを構造化し、多角的な分析によって**合格への最短ルートを特定する**ためのWebアプリケーション。

---

## 🎯 プロジェクトの目的

資格試験・各種試験の学習進捗を記録・可視化し、以下を実現します。

- 学習データの蓄積と推移の把握
- カテゴリ別の得点分析による**弱点の特定**
- 初回・前回・最新の比較による**成長の可視化**
- 合格に向けた**優先学習エリアの特定**

---

## 🖥️ 画面構成

| 画面名 | パス | 機能概要 |
|--------|------|----------|
| エントリ・ゲート | `/` | ユーザーIDによるログイン |
| ダッシュボード | `/dashboard` | 登録試験一覧・削除・各画面へのナビゲーション |
| ターゲット・レジストリ | `/registry` | 試験登録・カテゴリ追加・マスタからの読み込み |
| スコア入力 | `/score/:examId` | カテゴリ別スコア入力・履歴表示・編集・削除 |
| 分析 | `/analysis/:examId` | レーダーチャート・棒グラフによる得点率比較 |
| 出題範囲マスタ | `/master` | マスタカテゴリの登録・CSV読み込み・削除 |

---

## 🛠️ 技術スタック

| レイヤー | 技術 |
|----------|------|
| Frontend | Vue.js 3（TypeScript）+ Vite |
| Backend | FastAPI（Python 3.11） |
| Database | CSV ファイル（Pandas で集計） |
| グラフ描画 | ECharts + vue-echarts |

---

## 📁 ディレクトリ構成

```
my-study-tracker/
├── README.md
├── backend/
│   ├── venv/
│   └── app/
│       ├── main.py
│       ├── models/
│       │   ├── exam.py
│       │   ├── category.py
│       │   ├── score.py
│       │   └── master.py
│       ├── routers/
│       │   ├── exams.py
│       │   ├── categories.py
│       │   ├── scores.py
│       │   └── masters.py
│       └── services/
│           ├── csv_service.py
│           ├── category_service.py
│           ├── score_service.py
│           └── master_service.py
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── CategoryNode.vue
│       │   ├── ExamCard.vue
│       │   ├── ScoreRow.vue
│       │   ├── MasterNode.vue
│       │   └── MasterCheckNode.vue
│       ├── router/
│       │   └── index.ts
│       ├── stores/
│       │   ├── auth.ts
│       │   ├── exam.ts
│       │   ├── category.ts
│       │   ├── score.ts
│       │   └── master.ts
│       └── views/
│           ├── LoginView.vue
│           ├── DashboardView.vue
│           ├── TargetRegistryView.vue
│           ├── ScoreInputView.vue
│           ├── AnalysisView.vue
│           └── MasterView.vue
├── docs/
│   ├── README.md
│   ├── requirements.md
│   ├── environment-setup.md
│   └── troubleshooting.md
└── data/
    └── {user_id}/
        ├── {exam_id}/*.csv
        └── master/master_categories.csv
```

---

## ⚙️ 開発環境

| 項目 | バージョン |
|------|-----------| 
| macOS | 26.3|
| Python | 3.11.9（pyenv 2.6.23） |
| Node.js | 22.14.0（nodenv 1.6.2） |
| npm | 10.7.0 |

---

## 🚀 起動方法

### バックエンド

```bash
cd ~/my-study-tracker/backend
source venv/bin/activate
uvicorn app.main:app --reload
# → http://127.0.0.1:8000
```

### フロントエンド

```bash
cd ~/my-study-tracker/frontend
npm run dev
# → http://localhost:5173
```

---

## 📄 関連ドキュメント

- [ドキュメント一覧](./docs/README.md)
- [要件定義（RD）](./docs/requirements.md)
- [環境構築手順書](./docs/environment-setup.md)
- [トラブルシューティング](./docs/troubleshooting.md)
