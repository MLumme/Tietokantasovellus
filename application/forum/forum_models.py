from application import db
from sqlalchemy import event
#from application.auth.auth_models import User

association_table = db.Table("threadsubject", db.Model.metadata,
    db.Column("thread_id",db.Integer, db.ForeignKey('thread.id')),      
    db.Column("subject_id",db.Integer, db.ForeignKey('subject.id'))
)

class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default = db.func.current_timestamp())
    title = db.Column(db.String(200), nullable = False)
    messages = db.relationship("Message", cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    subjects = db.relationship("Subject", secondary=association_table)

    def __init__(self,title,user_id,subjects):
        self.title = title
        self.user_id = user_id
        self.subjects = subjects 

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    content = db.Column(db.String(1000), nullable = False)
    thread_id = db.Column(db.Integer,db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self,content,user_id):
        self.content = content
        self.user_id = user_id   

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)

    def __init__(self, name):
        self.name = name

#listens for addition of children to thread and updates last posts timestamp
@event.listens_for(Thread.messages, "append")
def receive_append_listener(target, value, initiator):
    target.date_edited = db.func.current_timestamp()
