Forum-project for TKT20011. Project provides for user a possibilty to register and log in on the forum view threads and their messages, add new threads and messages, and edit messages by themselves, and search for threads and messages. Additionally they can view their information such as number of posts made, change their password and usernames. In addition, there is a admin level user/s which can in addition of common user fuctionalities remove threads and messages, edit messages made by anyone, and view all users, remove them, promoten new admins, and add new subjects that can be used in thread creation and search.

Some notes on CRUD, both user and message tables have full implementation, but functions for user ar split btween auth_views and util_views.

Additional note on security, there are several if-statements and scripts in place that in normal use should newer activate if forum is used normally, as the buttons are not there if someone does not have admin-rights, but will (probaly) trigger if someone is sending post-requests using for example VS Codes Rest-client without admin-login, although I haven't tested it.

**Default Admin-accounts username is Admin, password is Password1234 (Yes, incredibly safe)**

[Location of the Heroku-app](https://arcane-temple-53433.herokuapp.com/forum/)

[User stories for current functionality.](documentation/user_stories.md)

[Final design for forum databases relational model](documentation/forum_relational_model.md)

Installation locally:
  * Virtual or not, install requirements from requirements.txt with `pip install -r requirements.txt` in root of the project.
  * Next, run `python3 manage.py create_admin`, which first create needed database-tables, locally will be in `application/forum.db`. Afterwards, and even in case of prexisting tables, inserts an Admin account and an deleted user account, details of admin-account  are provided above, but only if account-table is empty. on Heroku will be automatically run during deployment.
  * Run `python3 run.py`, go to `http://127.0.0.1:[PORT]/forum/`, replacing [PORT] with whatever your python has used, probably 5000.