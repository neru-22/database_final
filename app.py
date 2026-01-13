import os
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)

# DB設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://guest:password@postgres/my-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False) # カテゴリ追加
    deadline = db.Column(db.Date)

    # 期限が近いか（今日を含めて3日以内、または期限切れ）を判定する機能
    @property
    def is_urgent(self):
        if not self.deadline:
            return False
        today = date.today()
        # 期限切れ、または期限まで3日以内ならTrue
        return self.deadline <= today + timedelta(days=3)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>課題管理サイト</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: "Helvetica Neue", Arial, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background-color: #f4f4f9; }
        
        /* カードの基本スタイル */
        .card { background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: relative; border-left: 6px solid #ccc; }
        
        /* 優先度による色分け */
        .priority-高 { border-left-color: #ff4444; }
        .priority-中 { border-left-color: #ffbb33; }
        .priority-低 { border-left-color: #00C851; }

        /* ★期限切迫時の強調スタイル（全体を赤枠で囲む） */
        .urgent-alert { border: 2px solid #ff0000; background-color: #fff0f0; }
        .urgent-text { color: red; font-weight: bold; }

        /* カテゴリラベル */
        .category-badge {
            display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.8em; color: white; margin-right: 5px;
        }
        .cat-授業 { background-color: #5c6bc0; }
        .cat-バイト { background-color: #ef6c00; }
        .cat-プライベート { background-color: #8e24aa; }
        .cat-その他 { background-color: #78909c; }

        h1 { color: #333; }
        form { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 10px; }
        input, select, button { padding: 10px; width: 100%; box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #33b5e5; color: white; border: none; cursor: pointer; font-weight: bold; margin-top: 10px; }
        button:hover { opacity: 0.9; }
        .delete-btn { background-color: #ff4444; width: auto; float: right; padding: 5px 15px; margin-top: -5px;}
    </style>
</head>
<body>
    <h1>📋 タスク管理</h1>
    
    <form action="/add" method="POST">
        <div class="form-group">
            <input type="text" name="title" placeholder="タスク名を入力" required>
        </div>
        <div class="form-group" style="display: flex; gap: 10px;">
            <select name="category">
                <option value="授業">🏫 授業</option>
                <option value="バイト">💰 バイト</option>
                <option value="プライベート">🏠 プライベート</option>
                <option value="その他">📝 その他</option>
            </select>
            <select name="priority">
                <option value="高">優先度: 高</option>
                <option value="中">優先度: 中</option>
                <option value="低">優先度: 低</option>
            </select>
        </div>
        <div class="form-group">
            <input type="date" name="deadline">
        </div>
        <button type="submit">タスクを追加</button>
    </form>

    {% for task in tasks %}
    <div class="card priority-{{ task.priority }} {{ 'urgent-alert' if task.is_urgent else '' }}">
        
        <div>
            <span class="category-badge cat-{{ task.category }}">{{ task.category }}</span>
            {% if task.is_urgent %}
                <span class="urgent-text">⚠️ 期限間近！</span>
            {% endif %}
        </div>
        
        <h3 style="margin: 10px 0;">{{ task.title }}</h3>
        
        <p style="color: #666; font-size: 0.9em;">
            📅 期限: {{ task.deadline }} 
            {% if task.deadline %}
                (あと {{ (task.deadline - today).days }} 日)
            {% endif %}
        </p>
        
        <form action="/delete/{{ task.id }}" method="POST" style="background:none; padding:0; margin:0; box-shadow:none;">
            <button class="delete-btn">完了</button>
        </form>
        <div style="clear:both;"></div>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    try:
        tasks = Assignment.query.order_by(Assignment.deadline).all()
        return render_template_string(HTML_TEMPLATE, tasks=tasks, today=date.today())
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    priority = request.form.get('priority')
    category = request.form.get('category')
    date_str = request.form.get('deadline')
    
    deadline = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    
    new_task = Assignment(title=title, priority=priority, category=category, deadline=deadline)
    db.session.add(new_task)
    db.session.commit()
    return index()

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Assignment.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)