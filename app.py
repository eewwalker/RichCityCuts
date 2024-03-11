"""Flask App for Flask Cafe."""

import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Neighborhood, Stop


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///rich_city')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# spots


@app.get('/stops')
def stops_list():
    """Return list of all stops."""

    stops = Stop.query.order_by('name').all()

    return render_template(
        'stop/list.html',
        stops=stops,
    )


@app.get('/stops/<int:stop_id>')
def stop_detail(stop_id):
    """Show detail for stop."""

    stop = Stop.query.get_or_404(stop_id)

    return render_template(
        'stop/detail.html',
        stop=stop,
    )

@app.route('/stops/add', methods=['GET', 'POST'])
def add_stop():
    """ Show form if GET. If valid, add new stop and redirect"""
    
