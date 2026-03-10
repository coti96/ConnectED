import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

driver = db.get_db()
with driver.session() as session:
    result = session.run("MATCH (u:User) RETURN u.email as email, u.role as role, u.prenom as prenom")
    print(f"{'Email':<25} | {'Role':<15} | {'Prenom'}")
    print("-" * 50)
    for record in result:
        print(f"{record['email']:<25} | {record['role']:<15} | {record['prenom']}")
db.close()
