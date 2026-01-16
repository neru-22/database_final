# 📋 perfect assignment (タスク管理アプリ)

このプロジェクトは、Docker環境で動作するPython (Flask) と PostgreSQLを利用した、シンプルで直感的なタスク管理アプリケーションです。課題の優先度、カテゴリ、期限を管理し、期限の状態（期限切れ・期限間近）を自動的に判定して視覚的に警告する機能を備えています。

## 🚀 主な機能
* **タスクのCRUD操作**: タスクの登録(Create)、一覧表示(Read)、および削除(Delete)を網羅しています。
* **自動アラート判定**: 
    * 期限を過ぎたタスクには「🚨 期限を過ぎています」と表示。
    * 今日を含めて3日以内のタスクには「⚠️ 期限間近！」と警告。
* **視覚的な優先度管理**: 優先度（高・中・低）に応じて、カードの左線の色が赤・黄・緑に自動変化します。
* **カテゴリ分け**: 「授業」「バイト」「プライベート」「その他」のカテゴリごとにバッジを表示し、整理しやすくしています。

## 🛠 技術スタック
* **Backend**: Python 3.9 / Flask
* **Database**: PostgreSQL 16
* **ORM**: Flask-SQLAlchemy
* **Infrastructure**: Docker / Docker Compose

## 📦 システム構成 (Web 3 Layer)
本アプリは以下の3層構造で設計されています。
1.  **Presentation Layer**: FlaskによるHTMLテンプレートとCSSスタイル。
2.  **Application Layer**: Python/SQLAlchemyによるビジネスロジックとCRUD制御。
3.  **Data Layer**: PostgreSQL 16 によるデータの永続化。

## 🛠 起動方法

### 1. 前提条件
* Docker および Docker Compose がインストールされていること。

### 2. コンテナのビルドと起動
以下のコマンドを実行すると、DBの初期化とWebサーバーの起動が自動で行われます。
```bash
docker-compose up -d --build
