import sqlite3

conn = sqlite3.connect('errshare.db', timeout=5, isolation_level=None, check_same_thread=False)
cursor = conn.cursor()
