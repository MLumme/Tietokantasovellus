from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FormField, validators

class ThreadForm(FlaskForm):
    title = StringField("Title:", [validators.Length(min=1,max=200)])

    class Meta:
        csrf = False

class MessageForm(FlaskForm):
    message = TextAreaField("Message:", [validators.Length(min=1,max=1000)])

    class Meta:
        csrf = False

class NewThreadForm(FlaskForm):
    thread_title = FormField(ThreadForm)
    message_content = FormField(MessageForm)  