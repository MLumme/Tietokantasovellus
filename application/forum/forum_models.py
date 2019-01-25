from application import db

class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    title = db.Column(db.String(200), nullable = False)
    messages = db.relationship("Message")

    def __init__(self,title):
        self.title = title

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default = db.func.current_timestamp())
    content = db.Column(db.String(1000), nullable = False)
    thread_id = db.Column(db.Integer,db.ForeignKey('thread.id'))

    def __init__(self,content,thread_id):
        self.content = content
        self.thread_id = thread_id
