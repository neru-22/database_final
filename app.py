import os
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://guest:password@postgres/my-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    deadline = db.Column(db.Date)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Perfect Assignment</title>
    <meta charset="UTF-8">  <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }
        .card { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .priority-   { border-left: 5px solid #ff4444; }
        .priority-   { border-left: 5px solid #ffbb33; }
        .priority-   { border-left: 5px solid #00C851; }
        h1 { color: #333; }
        form { background: #fff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        input, select, button { padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        button { background-color: #33b5e5; color: white; border: none; cursor: pointer; }
        .delete-btn { background-color: #ff4444; width: auto; float: right; }
    </style>
</head>
<body>
    <h1>課題管理サイト</h1>
    
    <form action="/add" method="POST">
        <input type="text" name="title" placeholder="課題名" required>
        <select name="priority">
            <option value="  "> 提出課題:   </option>
            <option value="  "> 試験:   </option>
            <option value="  "> 自習:   </option>
        </select>
        <input type="date" name="deadline">
        <button type="submit"> 登録    </button>
    </form>

    {% for task in tasks %}
    <div class="card priority-{{ task.priority }}">
        <h3>{{ task.title }}</h3>
        <p>    : {{ task.deadline }} | priority : {{ task.priority }}</p>
        <form action="/delete/{{ task.id }}" method="POST" style="background:none; padding:0; margin:0;">
            <button class="delete-btn"> 完了</button>
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
        return render_template_string(HTML_TEMPLATE, tasks=tasks)
    except Exception as e:
        return f" G   [         ܂   : {str(e)}"

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    priority = request.form.get('priority')
    date_str = request.form.get('deadline')
    
    deadline = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    new_task = Assignment(title=title, priority=priority, deadline=deadline)
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