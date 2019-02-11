from application import db
#from application.auth.auth_models import User

class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    title = db.Column(db.String(200), nullable = False)
    messages = db.relationship("Message")
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self,title,user_id):
        self.title = title
        self.user_id = user_id

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    content = db.Column(db.String(1000), nullable = False)
    thread_id = db.Column(db.Integer,db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self,content,thread_id,user_id):
        self.content = content
        self.thread_id = thread_id  
        self.user_id = user_id   