from application import app, db
from application.forum.forum_models import Thread, Message
from application.forum.forum_forms import ThreadForm, MessageForm, NewThreadForm
from application.auth.auth_models import User
from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user

#show list of threads, eventually forum index
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
        new_thread_form = NewThreadForm()

        return render_template("forum/newthread.html", new_thread_form = new_thread_form)    

    #else extract form, add new entries for thread and message tables
    new_thread_form = NewThreadForm(request.form)

    thread = Thread(new_thread_form.thread_title.title.data,current_user.get_id())

    db.session().add(thread)
    db.session().flush()

    message = Message(new_thread_form.message_content.message.data,thread.id,current_user.get_id())

    db.session().add(message)
    db.session().commit()

    return redirect(url_for("thread_index"))

#view thread with given thread_id
@app.route("/forum/<thread_id>/", methods=["GET"])
@login_required
def thread_view(thread_id):
    thread_contents = db.session().query(Thread.id,Thread.title,Message,User.username,User.id).\
        filter(Thread.id == thread_id).\
        join(Message, Message.thread_id == Thread.id).\
        join(User, User.id == Message.user_id).all()
 
    messages = Message.query.filter(Message.thread_id == thread_id).order_by(Message.date_posted).all()

    message_form = MessageForm()

    return render_template("forum/showmessages.html", messages = messages, thread_id = thread_id, message_form = message_form, thread_contents = thread_contents)

#add new responses to thread
@app.route("/forum/<thread_id>/new", methods = ["GET","POST"])
@login_required
def thread_add(thread_id):

    if(request.method == "GET"):
        message_form = MessageForm()

        return render_template("forum/newmessage.html", message_form = message_form, thread_id = thread_id)


    message_form = MessageForm(request.form)

    if(not message_form.validate()):
        err = message_form.error
        return render_template("forum/newmessage.html", message_form = message_form, thread_id = thread_id, err=err)

    message = Message(message_form.message.data, thread_id, current_user.get_id())

    db.session.add(message)
    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))    

#edit message and commit changes, or remove
@app.route("/forum/message/<message_id>", methods = ["GET","POST","DELETE"])
@login_required
def msg_edit(message_id):
    message = Message.query.filter_by(id=message_id).one()

    if(request.method == "GET"):
        message_form = MessageForm()
        message_form.message.data = message.content
    
        return render_template("forum/editmessage.html", message = message, message_form = message_form)

    if(request.method == "DELETE"):
        thread_id = message.thread_id

        db.session.delete(message)
        db.session.commit()

        return redirect(url_for("thread_view", thread_id = thread_id))

    messageForm = MessageForm(request.form)

    if(not message_form.validate()):
        err = message_form.error
        return render_template("forum/editmessage.html", message = message, message_form = message_form, err=err)

    message.content = messageForm.message.data

    thread_id = message.thread_id

    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))