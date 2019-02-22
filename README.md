Repo for database project for course TKT20011, project subject web forum. Eventually will provide functionality for registration/login, posting of new threads and responses and removal of them, designation of thread subjects, and finally search functionality.

**Default Admin-accounts username is Admin, password is Password1234 (Yes, incredibly safe, and stored as plantext to be even more safe)**

[Location of the Heroku-app](https://arcane-temple-53433.herokuapp.com/forum/)

[User stories for current functionality.](documentation/user_stories.md)

[Final design for forum databases relational model](documentation/forum_relational_model.md)

Installation locally:
  * Virtual or not, install requirements from requirements.txt with `pip install -r requirements.txt` in root of the project.
  * Next, run `python3 manage.py create_admin`, which first create needed database-tables, locally will be in `application/forum.db`. Afterwards, and even in case of prexisting tables, inserts an Admin account, details of which has been given above, but only if account-table is empty. on Heroku will be automatically run during deployment.
  * Run `python3 run.py`, go to `http://127.0.0.1:[PORT]/forum/`, replacing [PORT] with whatever your python has used, probably 5000.

ToDo: 
  * Finish adding last valdations in place concerning messages.
  * Add checks in paths to check that functionalities meant for admins cannot be used by normal users even if they circumvent the lack of buttons and links to them in page views.
  * Encrypt passwords finally.
  * Implement user- and admin-utilities, eg. userprofiles, view of all users for admins for promoting other users to admins or deleting them.
  * Linked to above , in case of user deletion insert into database a deleted user entry where to link posts by deleted users, so that messages won't get orphaned from user relations.  
  * Finnish wotking on transfering everything to use Bootstrap-styles where usable.