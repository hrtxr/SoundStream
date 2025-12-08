import sqlite3

conn = sqlite3.connect('database.db')
with open ('Schema.sql') as f:
    conn.executescript(f.read())