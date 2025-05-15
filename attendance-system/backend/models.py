from .database import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                embedding vector(512) NOT NULL);
                """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                date DATE NOT NULL,
                session VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL)
                """)
    
    conn.commit()
    cur.close()
    conn.close()
    