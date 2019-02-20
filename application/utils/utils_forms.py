from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SelectField, validators, widgets
from application.forum.forum_models import Subject

"""
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label = False)
    option_widget = widgets.CheckboxInput()
"""

class SearchForm(FlaskForm):
    #subjects = [(subject.id, subject.name) for subject in Subject.query.all()]

    search = StringField("Search:", [validators.Length(min = 1, max = 200, message="Search string must be between 1 and 200 characters long"),validators.InputRequired(message = "Searchfield must not be empty")])
    search_from = SelectField("Search in:", choices=[("0", "User"),("1", "Thread title"),("2", "Message content")],validators=[validators.Required(message = "At least one location to search is needed")])
    search_subjects = SelectMultipleField("Select subjects:")#, choices = subjects)
    
    class Meta:
        csrf = False