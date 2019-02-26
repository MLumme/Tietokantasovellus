from flask_wtf import FlaskForm
from application.forum.forum_models import Subject
from wtforms import StringField, TextAreaField, FormField, SelectMultipleField, validators

class MessageForm(FlaskForm):
    message = TextAreaField("Message:", [validators.Length(min=1,max=1000, message="Message must be between 1 and 1000 characters")])

    class Meta:
        csrf = False

class ThreadForm(MessageForm):
    title = StringField("Title:", [validators.Length(min=1,max=200,message="Thread title must be between 1 and 200 characters")])
    message = MessageForm.message 
    subjects = SelectMultipleField("Select subjects:", choices=[])

    class Meta:
        csrf = False