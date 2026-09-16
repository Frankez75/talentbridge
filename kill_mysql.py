import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="talent_bridge"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW PROCESSLIST")
    processes = cursor.fetchall()
    
    my_id = conn.connection_id
    print(f"My connection ID: {my_id}")
    
    for row in processes:
        pid = row[0]
        state = row[6]
        info = row[7]
        
        if pid != my_id:
            print(f"Killing process {pid}, state: {state}, info: {info}")
            try:
                cursor.execute(f"KILL {pid}")
            except Exception as e:
                print(f"Could not kill {pid}: {e}")

    conn.commit()
    print("Done killing other processes")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
