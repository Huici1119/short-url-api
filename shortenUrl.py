from flask import Flask, request, jsonify, redirect, render_template
from datetime import datetime, timedelta
import validators
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)

#設定每分鐘最多5次
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

DB_PATH = 'url_data.db'

MAX_URL_LENGTH = 2048
EXPIRATION_DAYS = 30

# 資料庫初始化 
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT UNIQUE,
                original_url TEXT,
                expiration TIMESTAMP
            )
        ''')

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()

    original_url = data.get("original_url") if data else None

    # 檢查是否有輸入
    if not original_url:
        return jsonify({
            "short_url": "",
            "expiration_date": "",
            "success": False,
            "reason": "Missing 'original_url'"
        }), 400

    # 格式驗證
    if not validators.url(original_url):
        return jsonify({
            "short_url": "",
            "expiration_date": "",
            "success": False,
            "reason": "Invalid URL format"
        }), 400

    # 長度限制
    if len(original_url) > MAX_URL_LENGTH:
        return jsonify({
            "short_url": "",
            "expiration_date": "",
            "success": False,
            "reason": "URL too long"
        }), 400

    expiration_date = datetime.now() + timedelta(days=EXPIRATION_DAYS)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (short_id, original_url, expiration) VALUES (?, ?, ?)",
                    (None, original_url, expiration_date))
        short_id = str(cur.lastrowid)
        cur.execute("UPDATE urls SET short_id = ? WHERE id = ?", (short_id, cur.lastrowid))
        conn.commit()

    return jsonify({
        "short_url": f"http://localhost:5550/{short_id}",
        "expiration_date": expiration_date.isoformat(),
        "success": True,
        "reason": ""
    }), 201
    

@app.route('/<short_id>', methods=['GET'])
def redirect_short(short_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT original_url, expiration FROM urls WHERE short_id = ?", (short_id,))
        result = cur.fetchone()

    if not result:
        return jsonify({"error": "Invalid short URL"}), 404

    original_url, expiration = result
    if datetime.now() > datetime.fromisoformat(expiration):
        return jsonify({"error": "Short URL expired"}), 410

    return redirect(original_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
