import os
import time
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "notesdb"),
    )

def init_db():
    for _ in range(30):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "root"),
            )
            cur = conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS notesdb")
            cur.execute("USE notesdb")
            cur.execute("CREATE TABLE IF NOT EXISTS notes (id INT AUTO_INCREMENT PRIMARY KEY, content VARCHAR(255))")
            conn.commit()
            conn.close()
            return
        except Exception:
            time.sleep(2)

@app.route("/")
def home():
    return "Simple App Jenkins is running"

@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("INSERT INTO notes (content) VALUES (%s)", (request.json.get("content", ""),))
        conn.commit()
    cur.execute("SELECT id, content FROM notes")
    rows = [{"id": r[0], "content": r[1]} for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
