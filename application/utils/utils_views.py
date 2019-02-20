from application import app, db
from application.forum.forum_models import Thread, Message, Subject
from application.forum.forum_forms import ThreadForm, MessageForm, NewThreadForm
from application.utils.utils_forms import SearchForm
from application.auth.auth_models import User
from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.sql import text

#form for search functionality
@app.route("/forum/search/", methods = ["GET","POST"])
@login_required
def forum_search():
    #if get send to search form
    if(request.method == "GET"):
        search_form = SearchForm()

        subjects = [(subject.id, subject.name) for subject in Subject.query.all()]
        search_form.search_subjects.choices = subjects

        return render_template("utils/search.html", search_form = search_form)    

    #else extract form, run query to db and redirect
    search_form = SearchForm(request.form)

    print("KILOKILOKILOKILO")
    print(search_form.search.data)
    print(search_form.search_from.data)
    print(search_form.search_subjects.data)

    if(search_form.search_from.data == 0):
        stmt = text("SELECT * FROM account LEFT JOIN message "
                    "ON message.user_id = Account.id WHERE "
                    "Account.username LIKE '%:search%'").params(search = search_form.search.data)
    
    print(stmt)

    return redirect(url_for("thread_index"))

    """new_thread_form = NewThreadForm(request.form)

    thread = Thread(new_thread_form.thread_title.title.data,current_user.get_id())

    db.session().add(thread)
    db.session().flush()

    message = Message(new_thread_form.message_content.message.data,thread.id,current_user.get_id())

    db.session().add(message)
    db.session().commit()
    
    return redirect(url_for("thread_index"))
    """