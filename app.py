from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("portfolio.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Please fill in all fields"}), 400

    conn = sqlite3.connect("portfolio.db")
    conn.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": "Message saved successfully!"}), 201

@app.route("/")
def home():
    return open("index.html",
    encoding="utf-8").read()

if __name__ == "__main__":
    create_database()
    app.run(debug=True)