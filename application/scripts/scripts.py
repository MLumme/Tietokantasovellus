from flask_login import current_user
from flask import render_template

def test_if_admin_or_self(user_id):
    if(not(current_user.is_admin()) and (str(current_user.id) != user_id)):
        return render_template("error/incorrectrole.html")

    return    