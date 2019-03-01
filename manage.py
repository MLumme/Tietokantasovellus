from application import app, db, bcrypt
from application.auth.auth_models import User
from flask_script import Manager
import sys

manager = Manager(app)

@manager.command
def create_admin():
    db.create_all()

    if(User.query.all()):
        return

    admin = User("Admin", bcrypt.generate_password_hash("Password1234").decode('utf-8'))
    admin.admin = True
    
    db.session.add(admin)

    deleteduser = User("deleted user", bcrypt.generate_password_hash("Password1234").decode('utf-8'))
    deleteduser.id = 0

    db.session.add(deleteduser)

    db.session.commit()

if __name__ == "__main__":
    manager.run()