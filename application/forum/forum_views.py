from application import app, db
from flask import request, render_template, url_for, redirect
from application.forum.forum_models import Thread,Message

#show list of threads, eventually forum index
@app.route("/forum/", methods = ["GET"])
def thread_index():
    threads = Thread.query.all()
    return render_template("forum/showthreads.html", threads = threads)

#view thread with given thread_id
@app.route("/forum/<thread_id>/", methods=["GET"])
def thread_view(thread_id):
    messages = Message.query.filter(Message.thread_id == thread_id).order_by(Message.date_posted).all()

    return render_template("forum/showmessages.html", messages = messages, thread_id = thread_id)

#add a new thread and first message to db
@app.route("/forum/", methods=["POST"])
def thread_create():
    thread = Thread(request.form.get("title"))

    db.session().add(thread)
    db.session().flush()

    message = Message(request.form.get("contents"),thread.id)

    db.session().add(message)
    db.session().commit()

    return redirect(url_for("thread_index"))

#form for adding new threads
@app.route("/forum/newthread/")
def thread_new():
    return render_template("forum/newthread.html")    

#form for adding new responses to thread
@app.route("/forum/<thread_id>/new", methods = ["POST"])
def thread_add(thread_id):
    message = Message(request.form.get("contents"), thread_id)

    db.session.add(message)
    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))    

#remove message
@app.route("/forum/msgremove/<message_id>", methods = ["POST"])
def msg_remove(message_id):
    message = Message.query.filter_by(id=message_id).one()
    thread_id = message.thread_id

    db.session.delete(message)
    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))

#edit message
@app.route("/forum/msgedit/<message_id>", methods = ["GET"])
def msg_edit(message_id):
    message = Message.query.filter_by(id=message_id).one()

    return render_template("forum/editmessage.html", message = message)

#commit message edit
@app.route("/forum/msgeditcommit/<message_id>", methods = ["POST"])
def msg_edit_commit(message_id):
    message = Message.query.filter_by(id=message_id).one()

    message.content = request.form.get("contents")
    message.date_edited = db.func.current_timestamp()

    thread_id = message.thread_id

    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))