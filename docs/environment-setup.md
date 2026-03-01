# 環境構築手順書

> **対象プロジェクト**: 学習成績管理システム  
> **対象者**: 開発未経験〜初心者  
> **作成日**: 2026-03-01  
> **動作確認環境**: M5 MacBook Pro / macOS 26.3

---

## 📋 目次

1. [この手順書について](#1-この手順書について)
2. [全体の流れ（ロードマップ）](#2-全体の流れロードマップ)
3. [Homebrew のインストール](#3-homebrew-のインストール)
4. [Git のインストール・設定](#4-git-のインストール設定)
5. [GitHub アカウントの作成](#5-github-アカウントの作成)
6. [SSH キーの設定（GitHub 連携）](#6-ssh-キーの設定github-連携)
7. [Python 環境の構築（pyenv + Python 3.11）](#7-python-環境の構築pyenv--python-311)
8. [Node.js 環境の構築（nodenv + Node.js 20）](#8-nodejs-環境の構築nodenv--nodejs-20)
9. [VSCode の拡張機能インストール](#9-vscode-の拡張機能インストール)
10. [プロジェクトのリポジトリ作成](#10-プロジェクトのリポジトリ作成)
11. [動作確認チェックリスト](#11-動作確認チェックリスト)

---

## 1. この手順書について

### 前提条件

| 項目 | 状態 |
|------|------|
| MacBook Pro（M5） | ✅ 準備済み |
| macOS 26.3 | ✅ 確認済み |
| VSCode | ✅ インストール済み |
| Homebrew | ❌ これからインストール |
| Python | ❌ これからインストール |
| Node.js | ❌ これからインストール |
| GitHub アカウント | ❌ これからアカウント作成 |

### ターミナルの開き方

この手順書では **ターミナル（Terminal）** というアプリを頻繁に使います。

1. `Command（⌘）+ Space` を押して Spotlight 検索を開く
2. 「terminal」と入力して `Enter`
3. 黒または白い画面のウィンドウが開けば OK

> 💡 **コマンドの読み方**  
> `$` で始まる行はターミナルに入力するコマンドです。`$` 自体は入力しません。

---

## 2. 全体の流れ（ロードマップ）

```
[Step 1] Homebrew インストール   ← Mac のパッケージ管理ツール
     ↓
[Step 2] Git インストール・設定   ← バージョン管理ツール
     ↓
[Step 3] GitHub アカウント作成   ← コードの保管場所
     ↓
[Step 4] SSH キー設定            ← Mac と GitHub を安全につなぐ
     ↓
[Step 5] Python 環境構築         ← バックエンド（FastAPI）用
     ↓
[Step 6] Node.js 環境構築        ← フロントエンド（Vue.js）用
     ↓
[Step 7] VSCode 拡張機能         ← 開発を快適にする
     ↓
[Step 8] リポジトリ作成          ← プロジェクト開始！
```

---

## 3. Homebrew のインストール

**Homebrew** は Mac 用のパッケージ管理ツールです。これを使うと各種ツールを簡単にインストールできます。

### インストール

ターミナルを開いて以下のコマンドを貼り付け、`Enter` を押します。

```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

> ⚠️ **途中でパスワードを求められる場合があります。**  
> Mac のログインパスワードを入力してください（入力中は文字が表示されませんが、正しく入力されています）。

### パスの設定（M5 Mac では必須）

M1 以降の Apple Silicon Mac では、インストール後に**パスの追記**が必要です。

```bash
$ echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
$ eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 確認

```bash
$ brew --version
```

`Homebrew 4.x.x` のようにバージョンが表示されれば成功です。

---

## 4. Git のインストール・設定

**Git** はファイルの変更履歴を管理するツールです。

### インストール

```bash
$ brew install git
```

### 確認

```bash
$ git --version
# git version 2.x.x と表示されれば OK
```

### 初期設定（名前とメールアドレスの登録）

GitHub に登録する予定のメールアドレスを使用してください。

```bash
$ git config --global user.name "あなたの名前（例：Taro Yamada）"
$ git config --global user.email "あなたのメールアドレス"
```

### 設定確認

```bash
$ git config --list
```

`user.name` と `user.email` が表示されれば OK です。

---

## 5. GitHub アカウントの作成

GitHub はコードをオンラインで保管・管理するサービスです。

### アカウント作成手順

1. ブラウザで [https://github.com](https://github.com) を開く
2. **「Sign up」** をクリック
3. 以下を順番に入力・設定する

| 項目 | 入力内容 |
|------|----------|
| Email address | 使用するメールアドレス |
| Password | 安全なパスワード（12文字以上推奨） |
| Username | 半角英数字・ハイフンのみ（例：`taro-yamada`） |
| Email preferences | 任意 |

4. パズル認証（ロボット確認）を完了する
5. 届いたメールの認証コード（8桁）を入力する
6. 質問（チームの人数など）は「Skip personalization」でスキップ可

### 重要：プランの選択

- **Free（無料）** を選択して OK（本プロジェクトは無料プランで開発可能です）

---

## 6. SSH キーの設定（GitHub 連携）

SSH キーを使うと、毎回パスワードを入力せずに GitHub と通信できます。

### SSH キーの生成

```bash
$ ssh-keygen -t ed25519 -C "あなたのGitHubメールアドレス"
```

以下のように質問されます：

```
Enter file in which to save the key (/Users/ユーザー名/.ssh/id_ed25519):
```
→ そのまま `Enter`（デフォルトの場所に保存）

```
Enter passphrase (empty for no passphrase):
```
→ パスフレーズを設定する場合は入力（省略も可）。入力した場合は忘れずに。

### SSH エージェントへの登録

```bash
$ eval "$(ssh-agent -s)"
$ ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### 公開鍵を GitHub に登録する

```bash
# 公開鍵の内容をクリップボードにコピー
$ pbcopy < ~/.ssh/id_ed25519.pub
```

1. GitHub の右上アバターアイコン → **「Settings」**
2. 左メニュー → **「SSH and GPG keys」**
3. **「New SSH key」** をクリック
4. 以下を入力する

| 項目 | 入力内容 |
|------|----------|
| Title | `github_username` など識別しやすい名前 |
| Key type | `Authentication Key`（デフォルト） |
| Key | `Command+V` で貼り付け |

5. **「Add SSH key」** をクリック

### 接続テスト

```bash
$ ssh -T git@github.com
```

以下のように表示されれば成功です：

```
Hi ユーザー名! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 7. Python 環境の構築（pyenv + Python 3.11）

**pyenv** を使うとプロジェクトごとに Python のバージョンを切り替えられます。

### pyenv のインストール

```bash
$ brew install pyenv
```

### パスの設定

```bash
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
$ echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
$ echo 'eval "$(pyenv init -)"' >> ~/.zshrc
$ source ~/.zshrc
```

### Python 3.11 のインストール

```bash
$ pyenv install 3.11.9
$ pyenv global 3.11.9
```

> ⏳ インストールには数分かかります。

### 確認

```bash
$ python --version
# Python 3.11.9 と表示されれば OK

$ pip --version
# pip 23.x.x と表示されれば OK
```

---

## 8. Node.js 環境の構築（nodenv + Node.js 20）

フロントエンド（Vue.js）の開発に Node.js が必要です。

### nodenv のインストール

```bash
$ brew install nodenv
$ echo 'eval "$(nodenv init -)"' >> ~/.zshrc
$ source ~/.zshrc
```

### Node.js 20 のインストール

```bash
$ nodenv install 20.15.0
$ nodenv global 20.15.0
```

### 確認

```bash
$ node --version
# v20.15.0 と表示されれば OK

$ npm --version
# 10.x.x と表示されれば OK
```

---

## 9. VSCode の拡張機能インストール

VSCode を開き、以下の拡張機能をインストールします。

拡張機能のインストール方法：
1. VSCode 左サイドバーの **四角いアイコン（Extensions）** をクリック
2. 検索バーに拡張機能名を入力
3. **「Install」** をクリック

### 必須拡張機能

| 拡張機能名 | 用途 |
|------------|------|
| `Python` (Microsoft) | Python の補完・デバッグ |
| `Pylance` | Python の型チェック |
| `Vue - Official` | Vue.js のサポート |
| `TypeScript Vue Plugin (Volar)` | Vue + TypeScript |
| `ESLint` | JavaScript/TypeScript のコード品質チェック |
| `Prettier - Code formatter` | コード自動整形 |
| `GitLens` | Git の履歴・差分を見やすく表示 |
| `REST Client` | API のテスト（FastAPI 動作確認に便利） |

---

## 10. プロジェクトのリポジトリ作成

### GitHub でリポジトリを作成

1. GitHub の右上「**＋**」→「**New repository**」
2. 以下を設定する

| 項目 | 設定値 |
|------|--------|
| Repository name | `my-study-tracker` |
| Description | Learning Record and Weakness Analysis System |
| Visibility | `Private`（非公開） or `Public`（公開）|
| Add a README file | ✅ チェックを入れる |
| .gitignore | `Python` を選択 |
| License | 任意（`MIT License` 推奨） |

3. **「Create repository」** をクリック

### ローカルにクローン（ダウンロード）

```bash
# ホームディレクトリに移動
$ cd ~

# Devディレクトリを作成（任意）
$ mkdir Dev && cd Dev

# リポジトリをクローン（ユーザー名を自分のものに変更）
$ git clone git@github.com:あなたのユーザー名/my-study-tracker.git

# クローンしたフォルダに移動
$ cd my-study-tracker
```

### 基本的なディレクトリ構造を作成

```bash
$ mkdir -p backend frontend docs data
$ touch docs/README.md docs/requirements.md
```

### 変更をコミット＆プッシュ

```bash
$ git add .
$ git commit -m "docs: プロジェクト初期構成を追加"
$ git push origin main
```

GitHub のリポジトリページを開いて、ファイルが反映されていれば完成です！ 🎉

---

## 11. 動作確認チェックリスト

最後に全項目を確認してください。

```bash
# ✅ Homebrew
$ brew --version

# ✅ Git
$ git --version
$ git config user.name
$ git config user.email

# ✅ SSH（GitHub 接続）
$ ssh -T git@github.com

# ✅ Python
$ python --version

# ✅ pip
$ pip --version

# ✅ Node.js
$ node --version

# ✅ npm
$ npm --version
```

### 期待する出力例

| コマンド | 期待する出力 |
|----------|-------------|
| `brew --version` | `Homebrew 4.x.x` |
| `git --version` | `git version 2.x.x` |
| `python --version` | `Python 3.11.9` |
| `node --version` | `v20.15.0` |

---

## 🆘 トラブルシューティング

### `command not found: brew` と表示される

→ [Step 3「パスの設定」](#3-homebrew-のインストール) を再実行してください。

```bash
$ echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
$ source ~/.zprofile
```

### `pyenv: command not found` と表示される

→ `~/.zshrc` へのパス追記が反映されていない可能性があります。

```bash
$ source ~/.zshrc
```

### SSH 接続テストで `Permission denied` と表示される

→ SSH キーが GitHub に正しく登録されているか確認してください。  
→ [Step 6「公開鍵を GitHub に登録する」](#6-ssh-キーの設定github-連携) を再確認してください。

---

> 📝 **次のステップ**  
> 環境構築が完了したら、`docs/requirements.md` に要件定義（RD）を格納し、  
> Phase 1（FastAPI プロトタイプ）の開発に進んでください。