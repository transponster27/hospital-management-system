from database import get_connection

def run_schema():
    conn = get_connection()
    cur = conn.cursor()

    with open("schemas.sql", "r") as file:
        schema = file.read()
        cur.execute(schema)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_schema()
    print("Schema created successfully.")