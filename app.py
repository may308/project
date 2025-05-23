from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os


app = Flask(__name__)


@app.template_filter('add_stars')
def add_stars_filter(s):
    return f"★{s}★"


def init_db():
    if not os.path.exists('membership.db'):
        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS members (
                iid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                birthdate TEXT
            )
            '''
        )
        cursor.execute(
            '''
            INSERT OR IGNORE INTO members (
                username, email, password, phone, birthdate
            )
            VALUES (
                'admin', 'admin@example.com',
                'admin123', '0912345678', '1990-01-01'
            )
            '''
        )
        conn.commit()
        conn.close()


init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        phone = request.form['phone'].strip()
        birthdate = request.form['birthdate'].strip()

        if not username or not email or not password:
            return render_template(
                'error.html',
                message='請輸入用戶名、電子郵件和密碼'
            )

        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM members WHERE username = ?',
            (username,)
        )
        if cursor.fetchone():
            conn.close()
            return render_template(
                'error.html',
                message='用戶名已存在'
            )

        cursor.execute(
            '''
            INSERT INTO members (
                username, email, password, phone, birthdate
            )
            VALUES (?, ?, ?, ?, ?)
            ''',
            (username, email, password, phone, birthdate)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')