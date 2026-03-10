import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

driver = db.get_db()
with driver.session() as session:
    result = session.run("MATCH (u:User {email: 'student1@mail.com'}) RETURN u")
    if result.single():
        print("✅ student1@mail.com exists")
    else:
        print("❌ student1@mail.com DOES NOT exist")
db.close()
