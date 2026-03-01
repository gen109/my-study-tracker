# 学習成績管理システム（my-study-tracker）

> 学習データを構造化し、多角的な分析によって**合格への最短ルートを特定する**ためのWebアプリケーション。

---

## 🎯 プロジェクトの目的

資格試験・各種試験の学習進捗を記録・可視化し、以下を実現します。

- 学習データの蓄積と週次推移の把握
- カテゴリ別の得点分析による**弱点の特定**
- 初回・前回・最新の比較による**成長の可視化**
- 合格に向けた**優先学習エリアの特定**

---

## 🖥️ 画面構成

| 画面名 | 機能概要 |
|--------|----------|
| エントリ・ゲート | ログイン / 対象試験の切り替え |
| ターゲット・レジストリ | 試験登録・出題範囲・階層カテゴリの設定 |

---

## 🛠️ 技術スタック

| レイヤー | 技術 |
|----------|------|
| Frontend | Vue.js 3（TypeScript）+ Vite |
| Backend | FastAPI（Python 3.11） |
| Database | CSV ファイル（Pandas で集計） |
| グラフ描画 | ECharts または Chart.js |

---

## 📁 ディレクトリ構成

```
my-study-tracker/
├── backend/         # FastAPI（APIサーバー）
├── frontend/        # Vue.js（画面）
├── docs/            # ドキュメント類
│   ├── README.md          # このファイル
│   ├── requirements.md    # 要件定義（RD）
│   └── environment-setup.md  # 環境構築手順書
└── data/            # CSVデータ保存場所
    └── {user_id}/
        └── {exam_id}/
```

---

## 🗺️ 開発ロードマップ

### Phase 1 ： API Prototype（FastAPI）
- [ ] FastAPI プロジェクトセットアップ
- [ ] CSV 読み書きロジックの実装
- [ ] 階層カテゴリ管理 API の実装
- [ ] 比較ロジック（初回・前回・最新）の実装

### Phase 2 ： Repository Setup
- [ ] GitHub リポジトリの整備
- [ ] ディレクトリ構造の確定
- [ ] ドキュメントの格納

### Phase 3 ： Frontend Scaffold（Vue.js）
- [ ] UIデザインの実装
- [ ] FastAPI との連携

---

## ⚙️ 開発環境

| 項目 | バージョン |
|------|-----------|
| macOS | 26.3 |
| Python | 3.11.9 |
| Node.js | 20.15.0 |
| npm | 10.7.0 |
| pyenv | 2.6.23 |
| nodenv | 1.6.2 |

---

## 📄 関連ドキュメント

- [要件定義（RD）](./requirements.md)
- [環境構築手順書](./environment-setup.md)