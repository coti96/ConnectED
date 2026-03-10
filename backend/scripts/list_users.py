import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

driver = db.get_db()
with driver.session() as session:
    result = session.run("MATCH (u:User) RETURN u.email as email")
    emails = [record['email'] for record in result]
    print(f"Users found: {len(emails)}")
    for email in emails:
        print(f"- {email}")
db.close()
