from application import db
from sqlalchemy.sql import text
from application.db_base import base_model 

class User(base_model.Base):
    __tablename__ = "account"
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

    #find information on account and thread and postcounts for single user
    @staticmethod
    def get_user_info(user_id):
        stmt = text("SELECT account.id, account.username, account.admin, account.date_posted,"
                    " COUNT(DISTINCT thread.id) AS threadcount,"
                    " COUNT(DISTINCT message.id) AS postcount FROM account"
                    " LEFT JOIN thread ON thread.user_id = account.id"
                    " LEFT JOIN message ON message.user_id = account.id"
                    " WHERE account.id = :user_id GROUP BY account.id").params(user_id = user_id)
        user_info = db.engine.execute(stmt).fetchone()    

        return user_info

    #find above information on useres other than the one with user_id
    @staticmethod
    def get_all_user_info(user_id):
        stmt = text("SELECT account.id, account.username, account.admin, account.date_posted,"
                    " COUNT(DISTINCT thread.id) AS threadcount,"
                    " COUNT(DISTINCT message.id) AS postcount FROM account"
                    " LEFT JOIN thread ON thread.user_id = account.id"
                    " LEFT JOIN message ON message.user_id = account.id"
                    " WHERE account.id != :user_id AND account.id != 0 GROUP BY account.id").params(user_id = user_id)
        users_info = db.engine.execute(stmt)    

        return users_info        