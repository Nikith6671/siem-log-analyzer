import psycopg2
def connect_db():
    conn = psycopg2.connect(
        dbname = "siem_logs",
        user = "postgres",
        password = "6671",
        host = "localhost",
        port = "5432"   
    )
    return conn