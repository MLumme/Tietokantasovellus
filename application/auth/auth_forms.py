from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from application import db
from application.auth.auth_models import User

class LoginForm(FlaskForm):
    username = StringField("Username:", [validators.Required("Username missing")]) 
    password = PasswordField("Password:", [validators.Required("Password missing")])

    def validate(self):
        error = not FlaskForm.validate(self)

        #validate if username long enough
        if(len(self.username.data) < 5):
            err = "Username too short, minimum 5"
            self.username.errors.append(err)
            error = True

        #check if username too long
        if(len(self.username.data) > 200):    
            err = "Username too short, maximum 200"
            self.username.errors.append(err)
            error = True

        #validate if password long enough
        if(len(self.password.data) < 10):
            err = "Password too short, minimum 10"
            self.password.errors.append(err)
            error = True

        if(error):
            return False

        return True    

    class Meta:
        csrf = False

class RegForm(LoginForm):
    username = LoginForm.username 
    password = LoginForm.password
    password_repeat = PasswordField("Repeat password:", [validators.Required("Password confirmation missing")])  

    #custom validator
    def validate(self):
        error = not LoginForm.validate(self)

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
                self.username.errors.append(err)
                error = True

        if(error):
            return False

        return True
        
    class Meta:
        csrf = False
