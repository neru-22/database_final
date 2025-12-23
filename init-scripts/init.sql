-- 既存のデータがあれば削除して作り直す（リセット用）
DROP TABLE IF EXISTS assignments;

-- 課題管理用テーブルの作成
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,    -- 課題名
    priority VARCHAR(10) NOT NULL,  -- 優先順位 (高/中/低)
    deadline DATE,                  -- 提出期限
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 最初から入っているテストデータ
INSERT INTO assignments (title, priority, deadline) VALUES 
('データベース最終課題', '高', '2025-02-07'),
('サークルの合宿計画', '中', '2025-03-01'),
('バイトのシフト提出', '低', '2025-02-28');