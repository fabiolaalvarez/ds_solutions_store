# 1. Import statements
import sqlite3


# 2. Create a connection
s_con = sqlite3.connect('demo_data.sqlite3')


# 3. Create cursor object
s_cur = s_con.cursor()


# 4. Create table if not exist, then commit table
s_cur.execute("""CREATE TABLE IF NOT EXISTS demo(
    id SERIAL PRIMARY KEY,
    s VARCHAR(10) NOT NULL,
    x INTEGER,
    y INTEGER);""")

s_con.commit()


# 5. Insert data into table, then commit changes
s_cur.execute(
    """INSERT OR IGNORE INTO demo(id, s, x, y)
    VALUES ('0', 'g', '3', '9'), ('1', 'v', '5', '7'), ('2', 'f', '8', '7')""")

s_con.commit()


# 6. Create queries
row_count = s_cur.execute("SELECT COUNT(*) FROM demo").fetchall()

xy_at_least_5 = s_cur.execute(
    "SELECT COUNT(*) FROM demo WHERE x >= 5 AND y >= 5").fetchall()

unique_y = s_cur.execute("SELECT COUNT(DISTINCT y) FROM demo").fetchall()

# Test output
if __name__ == '__main__':
    print(row_count)
    print(xy_at_least_5)
    print(unique_y)
