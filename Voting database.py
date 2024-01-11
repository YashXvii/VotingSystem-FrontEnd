import os
import sqlite3

from flask import Flask, request, render_template

app = Flask(__name__)

DATABASE_PATH = "voting_system.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create the voter table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE
        )
    ''')

    # Create the candidates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    # Insert candidate names if not exists
    cursor.execute('INSERT OR IGNORE INTO candidates (name) VALUES ("Rahul")')
    cursor.execute('INSERT OR IGNORE INTO candidates (name) VALUES ("Abhi")')
    cursor.execute('INSERT OR IGNORE INTO candidates (name) VALUES ("Vatsal")')

    # Create the votes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT,
            candidate_id INTEGER,
            confirmed BOOLEAN,
            FOREIGN KEY (voter_id) REFERENCES voters (voter_id),
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    ''')

    conn.commit()
    conn.close()

if not os.path.exists(DATABASE_PATH):
    initialize_database()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Fetch candidate names
    cursor.execute('SELECT name FROM candidates')
    candidates = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template('index.html', candidates=candidates)

@app.route('/vote', methods=['POST'])
def vote():
    voter_id = request.form['voter_id']
    candidate_name = request.form['candidate']
    confirmation = request.form['confirmation']

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Check if the voter has already voted
    cursor.execute('SELECT * FROM voters WHERE voter_id=?', (voter_id,))
    existing_voter = cursor.fetchone()

    if existing_voter:
        return "You cannot vote again. You have already voted."

    # Fetch candidate ID
    cursor.execute('SELECT id FROM candidates WHERE name=?', (candidate_name,))
    candidate_id = cursor.fetchone()[0]

    # Insert vote into the database
    cursor.execute('''
        INSERT INTO votes (voter_id, candidate_id, confirmed)
        VALUES (?, ?, ?)
    ''', (voter_id, candidate_id, confirmation == 'Yes'))

    # Insert voter into the database
    cursor.execute('INSERT INTO voters (voter_id) VALUES (?)', (voter_id,))

    conn.commit()
    conn.close()

    return f"Thank you for voting. You voted for {candidate_name}."

if __name__ == "__main__":
    app.run(debug=True)
