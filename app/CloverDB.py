import sqlite3

class sqlite3_DB():
    def __init__(self, db="clover.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()