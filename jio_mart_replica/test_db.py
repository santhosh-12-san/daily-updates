import mysql.connector
from config import DB_CONFIG

try:
    print("Attempting to connect...")
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ SUCCESS! Connected to the database.")
    conn.close()
except mysql.connector.errors.ProgrammingError as e:
    if e.errno == 1045:
        print("❌ ERROR: Wrong Username or Password.")
        print("Please check 'config.py' again.")
    elif e.errno == 1049:
        print("❌ ERROR: Database 'jiomart_clone' does not exist.")
        print("Did you run the 'db.sql' script in Workbench?")
    else:
        print(f"❌ ERROR: {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")