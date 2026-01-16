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
    category = db.Column(db.String(20), nullable=False)
    deadline = db.Column(db.Date)
    is_completed = db.Column(db.Boolean, default=False) # 完了状態

    # 期限切れ判定
    @property
    def is_overdue(self):
        # 完了済み、または期限なしなら判定しない
        if self.is_completed or not self.deadline:
            return False
        return self.deadline < date.today()

    # 期限間近判定
    @property
    def is_urgent(self):
        if self.is_completed or not self.deadline:
            return False
        today = date.today()
        return today <= self.deadline <= today + timedelta(days=3)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>課題管理サイト</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: "Helvetica Neue", Arial, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background-color: #f4f4f9; }
        
        /* カード基本設定 */
        .card { background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: relative; border-left: 6px solid #ccc; transition: 0.3s; }
        
        /* 優先度（左線の色） */
        .priority-高 { border-left-color: #ff4444; }
        .priority-中 { border-left-color: #ffbb33; }
        .priority-低 { border-left-color: #00C851; }

        /* 警告アラート */
        .urgent-alert { border: 2px solid #ff4444; background-color: #fff0f0; }
        .urgent-text { color: #d32f2f; font-weight: bold; }

        .overdue-alert { border: 2px solid #7e57c2; background-color: #ede7f6; }
        .overdue-text { color: #512da8; font-weight: bold; background: #d1c4e9; padding: 2px 6px; border-radius: 4px; }

        /* ★完了済みタスクのデザイン（グレーアウト・打ち消し線） */
        .task-done {
            background-color: #eeeeee;
            border-left-color: #bbbbbb !important; /* 優先度色もグレーに */
            opacity: 0.7;
            border: 1px solid #ddd;
        }
        .task-done h3 { text-decoration: line-through; color: #888; }
        .task-done p { color: #999; }

        .category-badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.8em; color: white; margin-right: 5px; }
        .cat-授業 { background-color: #5c6bc0; }
        .cat-バイト { background-color: #ef6c00; }
        .cat-プライベート { background-color: #8e24aa; }
        .cat-その他 { background-color: #78909c; }
        
        h1 { color: #333; }
        form.add-form { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 10px; }
        input, select, button { padding: 10px; width: 100%; box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px; }
        
        /* ボタンのデザイン */
        .btn-add { background-color: #33b5e5; color: white; border: none; cursor: pointer; font-weight: bold; margin-top: 10px; }
        .btn-add:hover { opacity: 0.9; }

        /* 完了・削除ボタンの配置 */
        .action-buttons { float: right; display: flex; gap: 5px; margin-top: -10px; }
        
        .btn-complete { background-color: #00C851; color: white; border: none; cursor: pointer; padding: 5px 10px; border-radius: 4px; }
        .btn-undo { background-color: #999; color: white; border: none; cursor: pointer; padding: 5px 10px; border-radius: 4px; }
        .btn-delete { background-color: #ff4444; color: white; border: none; cursor: pointer; padding: 5px 10px; border-radius: 4px; }
        
        form.inline-form { display: inline; }
    </style>
</head>
<body>
    <h1>📋 タスク管理</h1>
    
    <form action="/add" method="POST" class="add-form">
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
        <button type="submit" class="btn-add">タスクを追加</button>
    </form>

    {% for task in tasks %}
    <div class="card priority-{{ task.priority }} {{ 'task-done' if task.is_completed else ('overdue-alert' if task.is_overdue else ('urgent-alert' if task.is_urgent else '')) }}">
        
        <div class="action-buttons">
            <form action="/complete/{{ task.id }}" method="POST" class="inline-form">
                {% if task.is_completed %}
                    <button class="btn-undo" title="未完了に戻す">↩️ 戻す</button>
                {% else %}
                    <button class="btn-complete" title="完了にする">✅ 完了</button>
                {% endif %}
            </form>

            <form action="/delete/{{ task.id }}" method="POST" class="inline-form" onsubmit="return confirm('本当に削除しますか？');">
                <button class="btn-delete" title="削除する">🗑️</button>
            </form>
        </div>

        <div>
            <span class="category-badge cat-{{ task.category }}">{{ task.category }}</span>
            
            {% if task.is_completed %}
                <span style="color:green; font-weight:bold;">✅ 完了済み</span>
            {% elif task.is_overdue %}
                <span class="overdue-text">🚨 期限を過ぎています</span>
            {% elif task.is_urgent %}
                <span class="urgent-text">⚠️ 期限間近！</span>
            {% endif %}
        </div>
        
        <h3 style="margin: 10px 0;">{{ task.title }}</h3>
        
        <p style="color: #666; font-size: 0.9em;">
            📅 期限: {{ task.deadline }} 
            {% if task.deadline and not task.is_completed %}
                {% set remaining = (task.deadline - today).days %}
                
                {% if remaining < 0 %}
                    <span style="color: #512da8; font-weight: bold;">
                        ({{ remaining * -1 }} 日経過しています)
                    </span>
                {% elif remaining == 0 %}
                    <span style="color: #d32f2f; font-weight: bold;">
                        (今日が期限です！)
                    </span>
                {% else %}
                    (あと {{ remaining }} 日)
                {% endif %}
            {% endif %}
        </p>
        
        <div style="clear:both;"></div>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    try:
        # 完了していないものを上に、完了済みを下に表示
        tasks = Assignment.query.order_by(Assignment.is_completed, Assignment.deadline).all()
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

# ★新機能: 完了状態の切り替え
@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    task = Assignment.query.get(id)
    if task:
        # TrueならFalseに、FalseならTrueにする（トグル）
        task.is_completed = not task.is_completed
        db.session.commit()
    return index()

# 削除機能（完全に消す）
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Assignment.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)