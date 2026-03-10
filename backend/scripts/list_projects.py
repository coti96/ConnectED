import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

driver = db.get_db()
with driver.session() as session:
    result = session.run("MATCH (p:Project) RETURN p.titre as title LIMIT 10")
    print("Projects found:")
    for record in result:
        print(f"- {record['title']}")
db.close()
