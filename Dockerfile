FROM python:3.9

WORKDIR /app

# 必要なツールをインストール
RUN pip install Flask Flask-SQLAlchemy psycopg2-binary

COPY . .

CMD ["python", "app.py"]