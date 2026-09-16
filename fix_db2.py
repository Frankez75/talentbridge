import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="talent_bridge"
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS alembic_version")
    conn.commit()
    print("Table alembic_version dropped successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
