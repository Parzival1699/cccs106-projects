import mysql.connector

def connect_db():
    """
    Tries to connect to the fletapp database using fletuser first.
    Falls back to root if fletuser fails.
    """
    try:
        # Try fletuser first
        conn = mysql.connector.connect(
            host="localhost",
            user="fletuser",
            password="password123",   
            database="fletapp",
            port=3306                 
        )
        print("✅ Connected with fletuser")
        return conn
    except mysql.connector.Error as err1:
        print(f"⚠️ fletuser connection failed: {err1}")
        try:
            # Fallback: try root
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password123",  # 👈 replace with your real root password
                database="fletapp",
                port=3307
            )
            print("✅ Connected with root")
            return conn
        except mysql.connector.Error as err2:
            print(f"❌ Root connection failed: {err2}")
            raise  # Re-raise the last error so main.py shows Database Error
