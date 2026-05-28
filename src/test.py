from database import get_connection, get_cursor

def test_connection():
    conn = None
    try:
        conn = get_connection()
        cur = get_cursor(conn)

        cur.execute("SELECT version();")
        print(cur.fetchone())

        cur.execute("SELECT current_database();")
        print(cur.fetchone())

        cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
        """)
        print(cur.fetchall())

    except Exception as e:
        print("Connection failed")
        print("Error:", e)

    finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    test_connection()

