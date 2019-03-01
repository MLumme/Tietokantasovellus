from application import app, db, bcrypt
from application.forum.forum_models import Thread, Message, Subject
from application.forum.forum_forms import ThreadForm, MessageForm, ThreadForm
from application.utils.utils_forms import SearchForm, SubjectForm
from application.auth.auth_models import User
from application.auth.auth_forms import PswChangeForm, UsrChangeForm
from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.sql import text
from application.scripts.scripts import test_if_admin_or_self

#functionality for user to view their information and delete themselves, or for 
# admin to do the same to other users 
@app.route("/util/user/<user_id>",methods = ["GET","POST"])
@login_required
def user_page(user_id):
    #allow rights to view or delete profile only to users themselves or admins
    test_if_admin_or_self(user_id)
     
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
            return redirect(url_for('auth_logout'))

        return redirect(url_for("thread_index")) 

    #else render infor on user and pages for password and username change
    user_info = User.get_user_info(user_id)

    password_change_form = PswChangeForm()
    username_change_form = UsrChangeForm()

    return render_template("utils/userpage.html", user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form)

#change password
@app.route("/util/user/<user_id>/changepsw",methods = ["POST"])
@login_required
def user_password(user_id):
    #check that user is attempting to change their own password, or is admin
    test_if_admin_or_self(user_id)

    password_change_form = PswChangeForm(request.form)
    username_change_form = UsrChangeForm()

    user_info = User.get_user_info(user_id)

    #validate that field imputs correct
    if(not password_change_form.validate()):
        err = password_change_form.errors
        return render_template("utils/userpage.html", user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form, err = err)

    #check if old password is correct
    user = User.query.get(user_id)

    if(not bcrypt.check_password_hash(user.password, password_change_form.old_password.data)):                
        err = {'Error':['Old password incorrect']}
        return render_template("utils/userpage.html", user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form, err = err)

    #replace password, commit to database
    user.password = bcrypt.generate_password_hash(password_change_form.new_password.data)
    db.session.commit()

    #if user changed own password logout
    if(str(current_user.id) == user_id):
        return redirect(url_for('auth_logout'))

    return render_template("utils/userpage.html", user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form)

#change username
@app.route("/util/user/<user_id>/changeusr",methods = ["POST"])
@login_required
def user_username(user_id):
    #check that user is attempting to change their own username, or is admin
    test_if_admin_or_self(user_id)

    username_change_form = UsrChangeForm(request.form)
    password_change_form = PswChangeForm()

    #validate that field imputs correct, also tests if new username is already taken
    if(not username_change_form.validate()):
        user_info = User.get_user_info(user_id)
        err = username_change_form.errors            
        return render_template("utils/userpage.html", user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form, err = err)

    #replace username, commit to database
    user = User.query.get(user_id)
    user.username = username_change_form.new_username.data

    db.session.commit()

    user_info = User.get_user_info(user_id)

    return render_template("utils/userpage.html", user_info = user_info, password_change_form = password_change_form, username_change_form = username_change_form)

#functionality for admins to view and manipulate users and add subjects to use in threads
@app.route("/util/admin", methods = ["GET","POST"])
@login_required
def forum_admin():
    if(not current_user.is_admin()):
        return redirect(url_for("thread_index"))

    if(request.method == "GET"):
        subject_form = SubjectForm()
        users = User.get_all_user_info(current_user.id)
        subjects = Subject.query.all()

        return render_template("utils/adminpage.html", subject_form = subject_form, users = users, subjects = subjects) 

    #add new subject
    subject_form = SubjectForm(request.form)

    subject = Subject(subject_form.subject.data)
    
    db.session.add(subject)
    db.session.commit()

    return redirect(url_for("forum_admin"))

#make user admin
@app.route("/util/user/<user_id>/admin",methods = ["POST"])
@login_required
def user_admin(user_id):
    #check if user is admin
    if(not current_user.is_admin()):
        return render_template("error/incorrectrole.html")

    user = User.query.get(user_id)

    #chec if user to be promoted is already an admin 
    if(user.is_admin()):
        err = {"error": ["user already admin"]}
        return redirect(url_for("forum_admin",err = err))

    user.admin = True
    db.session.commit()
    
    return redirect(url_for("forum_admin"))

#form for search functionality
@app.route("/util/search/", methods = ["GET","POST"])
@login_required
def forum_search():
    #if get send to search form
    if(request.method == "GET"):
        search_form = SearchForm()

        subjects = [(-1,"none")]
        subjects.extend([(subject.id, subject.name) for subject in Subject.query.all()])
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