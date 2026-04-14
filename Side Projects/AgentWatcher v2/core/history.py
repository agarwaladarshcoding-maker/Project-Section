import os
import sqlite3
from datetime import datetime

DB_DIR = os.path.expanduser('~/.agentwatch')
DB_PATH = os.path.join(DB_DIR, 'history.db')

def _init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                tool TEXT,
                event_type TEXT,
                full_message TEXT,
                buttons TEXT,
                user_response TEXT,
                resolved INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# Initialize on import
_init_db()

def log_event(tool: str, event_type: str, full_message: str, buttons: str) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO events (timestamp, tool, event_type, full_message, buttons)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, tool, event_type, full_message, buttons))
        conn.commit()
        return cursor.lastrowid

def mark_resolved(event_id: int, user_response: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE events 
            SET resolved = 1, user_response = ? 
            WHERE id = ?
        ''', (user_response, event_id))
        conn.commit()

def get_recent(n: int = 50) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM events 
            ORDER BY id DESC 
            LIMIT ?
        ''', (n,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
