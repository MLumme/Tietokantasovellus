from application import app,db
from application.auth.auth_models import User
from flask_script import Manager
import sys

manager = Manager(app)

@manager.command
def create_admin():
    db.create_all()

    if(User.query.all()):
        return

    admin = User("Admin","Password1234")
    admin.admin = True
    
    db.session.add(admin)
    db.session.commit()

if __name__ == "__main__":
    manager.run()