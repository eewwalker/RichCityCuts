"""Flask App for Flask Cafe."""

import os

from flask import Flask, render_template, redirect, flash, url_for, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from models import db, connect_db, Neighborhood, Stop, User
from forms import StopAddEditForm, CSRFProtectionForm, SignUpForm, LoginForm


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


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_form_to_g():
    """ Add a CSRF form so that any/every route can use it"""

    g.csrf = CSRFProtectionForm()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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
    form = StopAddEditForm()
    hoods = [(n.code, n.name) for n in Neighborhood.query.all()]
    form.hood_code.choices = hoods

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        hood_code = form.hood_code.data
        image_url = form.image_url.data

        stop = Stop(
            name=name,
            description=description,
            url=url,
            address=address,
            hood_code=hood_code,
            image_url=image_url
        )
        db.session.add(stop)
        db.session.commit()

        flash(f'{stop.name} added')
        return redirect(url_for('stop_detail', stop_id=stop.id))

    return render_template('stop/add-form.html', form=form)


@app.route('/stops/<int:stop_id>/edit', methods=['POST', 'GET'])
def edit_stop(stop_id):
    """ Show form if GET. If valid, edit form and redirect"""

    stop = Stop.query.get_or_404(stop_id)
    form = StopAddEditForm(obj=stop)

    hoods = [(n.code, n.name) for n in Neighborhood.query.all()]
    form.hood_code.choices = hoods

    if form.validate_on_submit():
        form.populate_obj(stop)
        db.session.commit()

        flash(f'{stop.name} edited')
        return redirect(url_for('stop_detail', stop_id=stop.id))

    return render_template('stop/edit-form.html', form=form)

#######################################
# user


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Handle user signup
        Create user, adds to DB and logs them in. Redirect to stops list
        If form not valid or GET show form
    """
    do_logout()

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                description=form.description.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()
            breakpoint()

        except IntegrityError:
            print('*************HEREinteERRRRRRR')
            flash(f'Username already taken', 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)
        flash(f'Hello, {user.username}')
        return redirect(url_for('stops_list'))

    else:
        print('*************HEREfinalelse')
        return render_template('auth/signup-form.html', form=form)
