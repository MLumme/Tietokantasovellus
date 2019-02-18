from application import db
#from application.forum.forum_models import Thread, Message

class User(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    username = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(200), nullable = False)
    admin = db.Column(db.Boolean, default = False)
    threads = db.relationship("Thread")
    messages = db.relationship("Message")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_admin(self):
        return self.admin