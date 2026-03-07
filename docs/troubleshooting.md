# トラブルシューティング

> 開発中に発生した問題と解決策をまとめたドキュメントです。

---

## 目次

1. [Python の lzma モジュールが見つからない](#1-python-の-lzma-モジュールが見つからない)
2. [GitHubの自動生成READMEが残ってしまう](#2-githubの自動生成readmeが残ってしまう)
3. [VSCode で Pylance のインポートエラーが出る](#3-vscode-で-pylance-のインポートエラーが出る)
4. [VSCode で Vetur の誤検知エラーが出る](#4-vscode-で-vetur-の誤検知エラーが出る)
5. [pinia-plugin-persistedstate 導入後に画面が真っ白になる](#5-pinia-plugin-persistedstate-導入後に画面が真っ白になる)
6. [npm run dev を wrong directory で実行してしまう](#6-npm-run-dev-を-wrong-directory-で実行してしまう)

---

## 1. Python の lzma モジュールが見つからない

### 症状

```
ModuleNotFoundError: No module named '_lzma'
WARNING: The Python lzma extension was not compiled. Missing the lzma lib?
```

### 原因

`xz` ライブラリが Homebrew にインストールされていない状態で Python をビルドしたため。

### 解決策

```bash
# xz をインストールしてから Python を再インストール
$ brew install xz
$ pyenv uninstall 3.11.9
$ pyenv install 3.11.9
$ pyenv global 3.11.9

# 確認
$ python -c "import lzma; print('lzma OK')"
```

### 教訓

pyenv で Python をインストールする前に `brew install xz` を実行すること。依存ライブラリのインストール順序が重要。

---

## 2. GitHubの自動生成READMEが残ってしまう

### 症状

GitHub でリポジトリ作成時に「Add a README file」をチェックすると、以下のような自動生成内容が残ってしまう。

```markdown
# my-study-tracker
Learning Record and Weakness Analysis System
```

### 原因

GitHub が自動生成した `README.md` が残ったまま、上書きが反映されていなかった。

### 解決策

ターミナルで直接上書きする。

```bash
$ cd ~/my-study-tracker
$ cat > README.md
```

カーソルが点滅したら `Control + C` を押して空ファイルにする。その後 VSCode で内容を貼り付けて保存する。

---

## 3. VSCode で Pylance のインポートエラーが出る

### 症状

```
インポート "fastapi.middleware.cors" を解決できませんでした Pylance
```

### 原因

VSCode が仮想環境（venv）の Python インタープリターを認識していなかった。

### 解決策

1. `Command + Shift + P` → 「Python: Select Interpreter」
2. 「Enter interpreter path...」を選択
3. 以下のパスを手動入力

```
/Users/gen109/my-study-tracker/backend/venv/bin/python
```

4. VSCode を再起動（`Command + Shift + P` → 「Developer: Reload Window」）

---

## 4. VSCode で Vetur の誤検知エラーが出る

### 症状

Vue 3 プロジェクトで以下のエラーが表示される。

```
Cannot find module '@/stores/auth' or its corresponding type declarations. Vetur(2307)
```

### 原因

Vetur は Vue 2 用の拡張機能のため、Vue 3 プロジェクトで誤検知が発生する。

### 解決策

1. VSCode の拡張機能パネルを開く
2. 「Vetur」を検索して**「無効にする」**
3. 「Vue - Official」を使用する
4. VSCode を再起動

---

## 5. pinia-plugin-persistedstate 導入後に画面が真っ白になる

### 症状

`pinia-plugin-persistedstate` をインストール後、画面が真っ白になりブラウザコンソールに以下のエラーが表示される。

```
Uncaught ReferenceError: pinia is not defined at main.ts:9
```

### 原因① Node.js のバージョン不足

`pinia-plugin-persistedstate` のインストールにより Vite が v7 にアップグレードされ、Node.js 20.15.0 では動作しなくなった。

```
You are using Node.js 20.15.0. Vite requires Node.js version 20.19+ or 22.12+.
```

**解決策**

```bash
$ nodenv install 22.14.0
$ nodenv global 22.14.0
$ node --version  # v22.14.0
```

### 原因② main.ts の記述ミス

`const pinia = createPinia()` が抜けていた。

**解決策**

```typescript
// ❌ 誤り
import { createPinia } from 'pinia'
pinia.use(piniaPluginPersistedstate)  // pinia が未定義

// ✅ 正しい
const pinia = createPinia()           // 必ずインスタンス化する
pinia.use(piniaPluginPersistedstate)
```

---

## 6. npm run dev を wrong directory で実行してしまう

### 症状

```
npm error code ENOENT
npm error path /Users/gen109/git/my-study-tracker/package.json
npm error enoent Could not read package.json
```

### 原因

`frontend/` ではなくプロジェクトルートで `npm run dev` を実行してしまった。

### 解決策

```bash
$ cd ~/my-study-tracker/frontend
$ npm run dev
```

### 教訓

`npm` コマンドは `package.json` があるフォルダで実行する必要がある。

| コマンド | 実行場所 |
|----------|---------|
| `npm run dev` | `frontend/` |
| `uvicorn app.main:app --reload` | `backend/` |
| `git` 操作 | プロジェクトルート（`my-study-tracker/`） |
