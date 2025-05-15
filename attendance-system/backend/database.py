import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="attendance_system",
            user="postgres",
            password="Shraya@17",
            port="5432"
        )

        print("Database connection successful")

        return conn

    except Exception as e:
        print("Error connecting to the database:", e)
        return None