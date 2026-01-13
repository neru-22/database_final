FROM python:3.9

WORKDIR /app

# 必要なツールをインストール
RUN pip install Flask Flask-SQLAlchemy psycopg2-binary

COPY . .

# 修正ポイント: カッコを使わない書き方に変更（こちらのほうがミスが起きにくいです）
CMD python app.py