from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FormField, SelectMultipleField, validators

class ThreadForm(FlaskForm):
    title = StringField("Title:", [validators.Length(min=1,max=200,message="Thread title must be between 1 and 200 characters")])

    class Meta:
        csrf = False

class MessageForm(FlaskForm):
    message = TextAreaField("Message:", [validators.Length(min=1,max=1000, message="Message must be between 1 and 1000 characters")])

    class Meta:
        csrf = False

class NewThreadForm(FlaskForm):
    thread_title = FormField(ThreadForm)
    message_content = FormField(MessageForm)  
    thread_subjects = SelectMultipleField("Select subjects:")
