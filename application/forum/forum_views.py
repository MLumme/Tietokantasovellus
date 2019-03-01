from application import app, db
from application.forum.forum_models import Thread, Message, Subject
from application.forum.forum_forms import MessageForm, ThreadForm
from application.auth.auth_models import User
from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user

#show list of threads
@app.route("/forum/", methods = ["GET"])
def thread_index():
    threads = Thread.query.all()
    return render_template("forum/showthreads.html", threads = threads)

#form for adding new threads and sending thrm to database
@app.route("/forum/newthread/", methods = ["GET","POST"])
@login_required
def thread_new():
    #if get send to thread creation form
    if(request.method == "GET"):
        thread_form = ThreadForm()

        subjects = [(subject.id, subject.name) for subject in Subject.query.all()]
        thread_form.subjects.choices += subjects
        
        return render_template("forum/newthread.html", thread_form = thread_form)    

    #else extract form, add new entries for thread and message tables
    subjects = [(subject.id, subject.name) for subject in Subject.query.all()]
    thread_form = ThreadForm(request.form)
    thread_form.subjects.choices += subjects

    if(not thread_form.validate_on_submit()):
        err = thread_form.errors
        return render_template("forum/newthread.html", thread_form = thread_form, err=err)

    subjects = Subject.query.filter(Subject.id.in_(thread_form.subjects.data)).all()

    thread = Thread(thread_form.title.data,current_user.get_id(),subjects)
    
    message = Message(thread_form.message.data,current_user.get_id())

    thread.messages = [message]

    db.session().add(thread)
    db.session().commit()
    
    return redirect(url_for("thread_index"))
    
#view thread with given thread_id, or delete it
@app.route("/forum/<thread_id>/", methods = ["GET","POST"])
@login_required
def thread_view(thread_id):
    #thread deletion
    if(request.method == "POST" and current_user.is_admin()):
        thread = Thread.query.get(thread_id)

        db.session().delete(thread)
        db.session().commit()

        return redirect(url_for("thread_index"))


    thread_contents = db.session().query(Thread.id,Thread.title,Message,User.username,User.id).\
        filter(Thread.id == thread_id).\
        join(Message, Message.thread_id == Thread.id).\
        join(User, User.id == Message.user_id).all()

    message_form = MessageForm()

    return render_template("forum/showmessages.html", thread_id = thread_id, message_form = message_form, thread_contents = thread_contents)



#add new responses to thread
@app.route("/forum/<thread_id>/new", methods = ["GET","POST"])
@login_required
def thread_add(thread_id):

    #if GET render form for new message
    if(request.method == "GET"):
        message_form = MessageForm()

        return render_template("forum/newmessage.html", message_form = message_form, thread_id = thread_id)

    #else send new message to db and update threads last modifiction date
    message_form = MessageForm(request.form)

    if(not message_form.validate()):
        err = message_form.errors
        return render_template("forum/newmessage.html", message_form = message_form, thread_id = thread_id, err=err)

    message = Message(message_form.message.data, current_user.get_id())
    
    thread = Thread.query.get(thread_id)
    thread.messages.append(message)

    db.session.merge(thread)
    db.session.flush()

    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))    

#edit message and commit changes
@app.route("/forum/message/<message_id>", methods = ["GET","POST"])
@login_required
def msg_edit(message_id):
    message = Message.query.get(message_id)

    #if GET render message edit form
    if(request.method == "GET"):
        message_form = MessageForm()
        message_form.message.data = message.content
    
        return render_template("forum/editmessage.html", message = message, message_form = message_form)

    #else submit edits to db and redirect to thread
    message_form = MessageForm(request.form)

    if(not message_form.validate()):
        err = message_form.errors
        return render_template("forum/editmessage.html", message = message, message_form = message_form, err=err)

    message.content = message_form.message.data

    thread_id = message.thread_id
    
    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))


#delete messages
@app.route("/forum/message/<message_id>/delete", methods = ["POST"])
@login_required
def msg_remove(message_id):
    if(current_user.is_admin()):
        message = Message.query.filter_by(id=message_id).one()

        thread_id = message.thread_id

        db.session.delete(message)
        db.session.commit()

        if(len(Thread.query.get(thread_id).messages) == 0):
            thread = Thread.query.get(thread_id)

            db.session().delete(thread)
            db.session().commit()

        return redirect(url_for("thread_index"))

    return redirect(url_for("thread_view", thread_id = thread_id))