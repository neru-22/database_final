-- 既存のデータがあれば削除して作り直す
DROP TABLE IF EXISTS assignments;

-- 課題管理用テーブルの作成
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    priority VARCHAR(10) NOT NULL,
    category VARCHAR(20) NOT NULL,  -- ★カテゴリを追加
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- テストデータ（カテゴリも含めて登録）
INSERT INTO assignments (title, priority, category, deadline) VALUES 
('データベース最終課題', '高', '授業', '2025-02-07'),
('サークルの合宿計画', '中', 'プライベート', '2025-03-01'),
('バイトのシフト提出', '低', 'バイト', '2025-02-28');