import sqlite3
import random
import string

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def db_init():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS urls (id TEXT, url TEXT)")

def create_url(url):
    while True:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        code = generate_code()
        cursor.execute("SELECT id FROM urls WHERE id = ?", (code,))
        data = cursor.fetchone()

        if not data:
            cursor.execute("INSERT INTO urls (id, url) VALUES (?, ?)", (code, url,))
            db.commit()
            return code

def get_url(link_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT url FROM urls WHERE id = ?", (link_id,))
    data = cursor.fetchone()
    
    if data:
        return data[0]
    else:
        return False

db_init()