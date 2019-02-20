from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from application import db
from application.auth.auth_models import User

#class for username and pasword needed for login
class LoginForm(FlaskForm):
    username = StringField("Username:", [validators.Required("Username missing"), validators.Length(min=4, max=200, message="Username must be between 5 and 200 characters long")]) 
    password = PasswordField("Password:", [validators.Required("Password missing"), validators.Length(min=4, max=200, message="Password must be between 10 and 200 characters long")])
   
    class Meta:
        csrf = False

#class for registration form, inherits Loginform and its validators
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
                err = "Username already taken"
                self.username.errors.append(err)
                error = True

        if(error):
            return False

        return True
        
    class Meta:
        csrf = False
