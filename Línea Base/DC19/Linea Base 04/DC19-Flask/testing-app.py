import sys
sys.path.append("..")

from app import create_app, db
from app.models import Role

def test_server():
    at = create_app("testing")
    at.app_context().push()
    db.create_all()
    Role.insert_roles()
    at.run()

if __name__ == '__main__':
    test_server()