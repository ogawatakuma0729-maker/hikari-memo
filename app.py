import os
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

JST = timezone(timedelta(hours=9))
BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DATABASE_PATH", BASE / "data.db"))

app = Flask(__name__)


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/submit")
def submit():
    name = (request.form.get("name") or "").strip()
    body = (request.form.get("body") or "").strip()
    if not name or not body:
        return render_template("index.html", error="名前と内容を入力してください。"), 400
    if len(name) > 40 or len(body) > 400:
        return render_template("index.html", error="文字数が多すぎます。"), 400
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO notes (name, body, created_at) VALUES (?, ?, ?)",
            (name, body, now),
        )
    return redirect(url_for("notes"))


@app.route("/notes")
def notes():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT name, body, created_at FROM notes ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return render_template("notes.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
