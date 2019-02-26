from application import app, db
from application.forum.forum_models import Thread, Message, Subject
from application.forum.forum_forms import ThreadForm, MessageForm, ThreadForm
from application.utils.utils_forms import SearchForm
from application.auth.auth_models import User
from application.auth.auth_forms import PswChangeForm, UsrChangeForm
from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.sql import text

#functionality for user to view their information and delete themselves, or for 
# admin to do the same to other users 
@app.route("/forum/user/<user_id>",methods = ["GET","POST"])
@login_required
def user_page(user_id):
    #allow rights to view or delete profile only to users themselves or admins
    if(not(current_user.is_admin()) and (str(current_user.id) != user_id)):
        err = {"privilegeerror": ["Insufficient user privileges to use this function"]}
        return render_template("forum/showthreads.html",err=err) 
     
    #delete user 
    if(request.method == "POST"):
        threads = Thread.query.filter_by(user_id = user_id).all()

        for thread in threads:
            thread.user_id = 0
        
        messages = Message.query.filter_by(user_id = user_id).all()

        for message in messages:
            message.user_id = 0

        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()

        #if user deleted themselves redirect to logout, else sen back to thread index
        if(current_user.id == user_id):
            return render_template(url_for('auth_logout'))

        return redirect(url_for("thread_index")) 

    #else render infor on user and pages for password and username change
    stmt = text("SELECT account.id, account.username, account.date_posted,"
                " COUNT(DISTINCT thread.id) AS threadcount,"
                " COUNT(DISTINCT message.id) AS postcount FROM account"
                " LEFT JOIN thread ON thread.user_id = account.id"
                " LEFT JOIN message ON message.user_id = account.id"
                " WHERE account.id = :user_id GROUP BY account.id").params(user_id = user_id)
    user_info = db.engine.execute(stmt).fetchone()

    password_change_form = PswChangeForm()
    username_change_form = UsrChangeForm()

    return render_template("utils/userpage.html",user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form)

@app.route("/forum/user/<user_id>/changepsw",methods = ["POST"])
@login_required
def user_password(user_id):
    return redirect(url_for("thread_index")) 

@app.route("/forum/user/<user_id>/changeusr",methods = ["POST"])
@login_required
def user_username(user_id):
    return redirect(url_for("thread_index"))
 
#form for search functionality
@app.route("/forum/search/", methods = ["GET","POST"])
@login_required
def forum_search():
    #if get send to search form
    if(request.method == "GET"):
        search_form = SearchForm()

        subjects = [(-1,"none")]
        subjects.extend([(subject.id, subject.name) for subject in Subject.query.all()])
        print(subjects)
        search_form.search_subjects.choices = subjects

        return render_template("utils/search.html", search_form = search_form)    

    #else extract form, run query to db and redirect
    search_form = SearchForm(request.form)

    #ctract searchstring, subject id, and integer denoting on ehat the search is done on
    search = search_form.search.data 
    where = search_form.search_from.data
    subject = search_form.search_subjects.data  

    #search messages and threads by username
    if(where == "0"):
        if(subject == "-1"):
            stmt = text("SELECT thread.* FROM thread"
                        " INNER JOIN account ON LOWER(account.username) LIKE LOWER('%' || :search || '%')"
                        " AND account.id = thread.user_id"
                        " ORDER BY thread.id").params(search = search)
            thread_search = db.engine.execute(stmt)           

            stmt = text("SELECT thread.id, thread.title, account.id, account.username, message.* FROM thread" 
                        " INNER JOIN message ON message.thread_id = thread.id" 
                        " INNER JOIN account ON LOWER(account.username) LIKE LOWER('%' || :search || '%')" 
                        " AND account.id = message.user_id" 
                        " ORDER BY thread.id").params(search = search)
            message_search = db.engine.execute(stmt)
        else:   
            stmt = text("SELECT thread.* FROM threadsubject" 
                        " INNER JOIN thread ON threadsubject.thread_id = thread.id"
                        " INNER JOIN account ON LOWER(account.username) LIKE LOWER('%' || :search || '%')"
                        " AND account.id = thread.user_id"
                        " WHERE threadsubject.subject_id = :subject"
                        " ORDER BY thread.id").params(search = search, subject = subject)
            thread_search = db.engine.execute(stmt)
            
            stmt = text("SELECT thread.id, thread.title, account.id, account.username, message.* FROM threadsubject" 
                        " INNER JOIN thread ON threadsubject.thread_id = thread.id" 
                        " INNER JOIN message ON message.thread_id = thread.id" 
                        " INNER JOIN account ON LOWER(account.username) LIKE LOWER('%' || :search || '%')" 
                        " AND account.id = message.user_id" 
                        " WHERE threadsubject.subject_id = :subject" 
                        " ORDER BY thread.id").params(search = search, subject = subject)
            message_search = db.engine.execute(stmt)

        return render_template("utils/searchresults.html", message_search = message_search, thread_search = thread_search)

    #search by thread title
    elif(where == "1"):
        if(subject == "-1"):
            stmt = text("SELECT thread.* FROM thread"
                        " WHERE LOWER(thread.title) LIKE LOWER('%' || :search || '%')"
                        " ORDER BY thread.id").params(search = search)
            thread_search = db.engine.execute(stmt)

        else:
            stmt = text("SELECT thread.* FROM threadsubject"
                        " INNER JOIN thread ON threadsubject.thread_id = thread.id"
                        " AND LOWER(thread.title) LIKE LOWER('%' || :search || '%')"
                        " WHERE threadsubject.subject_id = :subject "
                        " ORDER BY thread.id").params(search = search, subject = subject)
            thread_search = db.engine.execute(stmt)

        return render_template("utils/searchresults.html", thread_search = thread_search)

    #search by message contents    
    elif(where == "2"):
        if(subject == "-1"):
            stmt = text("SELECT thread.id, thread.title, account.id, account.username, message.* FROM thread "
                        " INNER JOIN message ON message.thread_id = thread.id"
                        " AND LOWER(message.content) LIKE LOWER('%' || :search || '%')"
                        " INNER JOIN account ON account.id = message.user_id"
                        " ORDER BY thread.id").params(search = search)
            message_search = db.engine.execute(stmt)       
        else:       
            stmt = text("SELECT thread.id, thread.title, account.id, account.username, message.* FROM threadsubject"
                        " INNER JOIN thread ON threadsubject.thread_id = thread.id"
                        " INNER JOIN message ON message.thread_id = thread.id"
                        " AND LOWER(message.content) LIKE LOWER('%' || :search || '%')"
                        " INNER JOIN account ON account.id = message.user_id"
                        " WHERE threadsubject.subject_id = :subject "
                        " ORDER BY thread.id").params(search = search, subject = subject)
            message_search = db.engine.execute(stmt)

        return render_template("utils/searchresults.html", message_search = message_search)

    #something very wrong has happpened te end up here and I don't even know how
    else:
        return render_template("forum/showthreads.html")