from db import connect_db

def detect_failed_logins():
    conn = connect_db()
    cur = conn.cursor()

    query = """
    SELECT message, COUNT(*) 
    FROM logs 
    WHERE level = 'WARNING'
    GROUP BY message
    """

    cur.execute(query)
    results = cur.fetchall()

    print("\n🔍 Threat Analysis Report:\n")

    for message, count in results:
        if count > 3:
            print(f"⚠️ ALERT: {message} → {count} times")
        else:
            print(f"✔ {message} → {count} times")

    cur.close()
    conn.close()

if __name__ == "__main__":
    detect_failed_logins()