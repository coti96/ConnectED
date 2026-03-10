import sys
import os

# Add parent directory to path to import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from flask_bcrypt import Bcrypt

def reset_passwords():
    print("Generating hash for 'password'...")
    # Initialize Bcrypt (no app needed for hash generation usually, but let's check)
    bcrypt = Bcrypt()
    pw_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    print(f"Hash generated: {pw_hash}")

    print("Connecting to database...")
    driver = db.get_db()
    
    with driver.session() as session:
        # Update ALL users with the new password hash
        result = session.run("""
        MATCH (u:User) 
        SET u.password_hash = $hash 
        RETURN count(u) as count
        """, hash=pw_hash)
        
        count = result.single()['count']
        print(f"✅ Successfully updated {count} users with password 'password'")

if __name__ == "__main__":
    try:
        reset_passwords()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
