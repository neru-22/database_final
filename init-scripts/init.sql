-- 既存のデータがあれば削除して作り直す
DROP TABLE IF EXISTS assignments;

-- 課題管理用テーブルの作成
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    priority VARCHAR(10) NOT NULL,
    category VARCHAR(20) NOT NULL,
    deadline DATE,
    is_completed BOOLEAN DEFAULT FALSE, -- ★完了フラグを追加
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- テストデータ（カテゴリも含めて登録）
INSERT INTO assignments (title, priority, category, deadline, is_completed) VALUES 
('データベース最終課題', '高', '授業', '2025-02-07', FALSE),
('終わった掃除', '低', 'プライベート', '2025-01-10', TRUE), -- 完了済みのテストデータ
('バイトのシフト提出', '低', 'バイト', '2025-02-28', FALSE);