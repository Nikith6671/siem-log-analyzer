from db import connect_db

def insert_logs():
    conn = connect_db()
    cur = conn.cursor()

    with open("logs/system.log", "r") as file:
        for line in file:
            parts = line.split(" - ")

            timestamp = parts[0].replace(",", ".")
            level = parts[1]
            message = parts[2].strip()

            cur.execute(
                "INSERT INTO logs (timestamp, level, message) VALUES (%s, %s, %s)",
                (timestamp, level, message)
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Logs inserted into database!")

if __name__ == "__main__":
    insert_logs()