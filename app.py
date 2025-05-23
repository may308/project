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