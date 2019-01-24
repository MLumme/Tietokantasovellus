from application import app, db
from flask import request, render_template, url_for, redirect
from application.forum.forum_models import Thread,Message

#show list of threads, eventually forum index
@app.route("/forum", methods = ["GET"])
def thread_index():
    threads = Thread.query.all()
    return render_template("forum/showthreads.html", threads = threads)

#view thread with given thread_id
@app.route("/forum/<thread_id>/", methods=["GET"])
def thread_view(thread_id):
    messages = Message.query.filter(Message.thread_id == thread_id).all()

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
def thread_form():
    return render_template("forum/newthread.html")    

#form for adding new responses to thread
@app.route("/forum/<thread_id>/new", methods = ["POST"])
def thread_add(thread_id):
    message = Message(request.form.get("contents"), thread_id)

    db.session.add(message)
    db.session.commit()

    return redirect(url_for("thread_view", thread_id = thread_id))    