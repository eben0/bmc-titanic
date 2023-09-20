if __name__ == "__main__":
    import sqlite3
    DB_PATH = "/app/data/titanic.db"
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = db.cursor()
    cnt = cur.execute("SELECT COUNT(*) FROM titanic").fetchone()
    print(f"Found {cnt[0]} results")
