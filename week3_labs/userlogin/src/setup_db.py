import mysql.connector

def setup_database():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",             # 👈 change if you use another MySQL user
            password="your_password" # 👈 put your actual password here
        )
        cursor = conn.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS fletapp;")
        cursor.execute("USE fletapp;")

        # Drop and recreate users table
        cursor.execute("DROP TABLE IF EXISTS users;")
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            );
        """)

        # Insert default user
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES ('testuser', 'password123');
        """)

        conn.commit()
        print("✅ Database reset: users table recreated with default account.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
