from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from application import db
from application.auth.auth_models import User

class RegForm(FlaskForm):
    username = StringField("Username:") 
    password = PasswordField("Password:")
    password_repeat = PasswordField("Repeat password:")  

    #custom validator
    def validate(self):
        FlaskForm.validate(self)

        error = False

        #validate if username long enough
        if(len(self.username.data) < 5):
            err = "Username too short, minimum 5"
            self.username.errors.append(err)
            error = True

        #validate if password long enough
        if(len(self.password.data) < 10):
            err = "Password too short, minimum 10"
            self.password.errors.append(err)
            error = True

        #test if password and repeat matches
        if(self.password.data != self.password_repeat.data):
            err = "Passwords do not match"
            self.password.errors.append(err)
            error = True

        #if one of the above won't validate don't bother querying the database
        if(not error):

            user = User.query.filter_by(username = self.username.data).first()

            #test if preexisting user has same username
            if(user):
                print("kilo")
                err = "Username taken"
                self.username.errors.append(err)
                error = True

        if(error):
            return False

        return True
        
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    username = StringField("Username:", [validators.Length(min=5,max=200)]) 
    password = PasswordField("Password:", [validators.Length(min=10)])

    class Meta:
        csrf = False
