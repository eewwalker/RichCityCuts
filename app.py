"""Flask App for Flask Cafe."""

import os

from flask import Flask, render_template, redirect, flash, url_for, session, \
    g, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from models import db, connect_db, Neighborhood, Stop, User, DEFAULT_IMG_URL, \
    DEFAULT_STOP_URL
from forms import StopAddEditForm, CSRFProtectionForm, SignUpForm, LoginForm, \
    ProfileEditForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///rich_city')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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

    g.csrf_form = CSRFProtectionForm()


@app.errorhandler(404)
def page_not_found(e):
    """ Custom 404 page to render """
    return render_template('404.html'), 404


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

    if not g.user:
        flash('Please log in or Sign up!', 'danger')
        return redirect(url_for('homepage'))

    stops = Stop.query.order_by('name').all()

    return render_template(
        'stop/list.html',
        stops=stops,
    )


@app.get('/stops/<int:stop_id>')
def stop_detail(stop_id):
    """Show detail for stop."""
    if not g.user:
        flash('Please log in or Sign up!', 'danger')
        return redirect(url_for('homepage'))

    stop = Stop.query.get_or_404(stop_id)

    return render_template(
        'stop/detail.html',
        stop=stop,
    )


@app.route('/stops/add', methods=['GET', 'POST'])
def add_stop():
    """ Show form if GET. If valid, add new stop and redirect
        Can only be done by admin"""

    if not g.user:
        flash('Please log in or Sign up!', 'danger')
        return redirect(url_for('homepage'))

    if g.user.admin:
        form = StopAddEditForm()

        hoods = [(n.code, n.name) for n in Neighborhood.query.all()]
        form.hood_code.choices = hoods

        if form.validate_on_submit():

            stop = Stop(
                name=form.name.data,
                description=form.description.data,
                url=form.url.data,
                address=form.address.data,
                hood_code=form.hood_code.data,
                image_url=form.image_url.data or DEFAULT_STOP_URL
            )
            db.session.add(stop)
            db.session.commit()

            stop.save_map()

            flash(f'{stop.name} added', 'success')
            return redirect(url_for('stop_detail', stop_id=stop.id))

        return render_template('stop/add-form.html', form=form)

    return redirect(url_for('homepage'))


@app.route('/stops/<int:stop_id>/edit', methods=['POST', 'GET'])
def edit_stop(stop_id):
    """ Show form if GET. If valid, edit form and redirect
        Can only be done by admin """

    if not g.user:
        flash('Please log in or Sign up!', 'danger')
        return redirect(url_for('homepage'))

    if g.user.admin:

        stop = Stop.query.get_or_404(stop_id)
        form = StopAddEditForm(obj=stop)

        hoods = [(n.code, n.name) for n in Neighborhood.query.all()]
        form.hood_code.choices = hoods

        if form.validate_on_submit():
            if form.address.data:
                form.populate_obj(stop)
                db.session.flush()
                stop.save_map()

            form.populate_obj(stop)
            db.session.commit()

            flash(f'{stop.name} edited', 'success')
            return redirect(url_for('stop_detail', stop_id=stop.id))

        return render_template('stop/edit-form.html', form=form)

    return redirect(url_for('homepage'))


@app.post('/stops/<int:stop_id>/delete')
def delete_stop(stop_id):
    """ Delete stop if admin"""

    if not g.user and not g.user.admin:
        flash('Please log in or Sign up!', 'danger')
        return redirect(url_for('homepage'))

    stop = Stop.query.get_or_404(stop_id)

    g.user.liked_stops.remove(stop)
    db.session.delete(stop)
    db.session.commit()

    return redirect(url_for('stops_list'))


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

        except IntegrityError:
            db.session.rollback()
            flash(f'Username already taken', 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)

        flash(f'Hello, {user.username}', 'success')
        return redirect(url_for('stops_list'))

    else:
        return render_template('auth/signup-form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handle user login
        If GET show login form
        Process login, log in user redirect to stop list
       """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )
        if user:
            do_login(user)

            flash(f'Hello, {user.username}', 'success')
            return redirect(url_for('stops_list'))

        flash("Invalid credentials", 'error')
    return render_template('auth/login-form.html', form=form)


@app.post('/logout')
def logout():
    """ Logout user"""

    if g.csrf_form.validate_on_submit():
        do_logout()

        flash(f'Successfully logged out')
        return redirect(url_for('homepage'))
    else:
        flash(f'You do not have access', 'danger')
        raise Unauthorized()


@app.get('/users/<int:user_id>')
def show_user_profile(user_id):
    """ Show profile page about user """

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect(url_for('homepage'))

    user = User.query.get_or_404(user_id)
    return render_template('profile/detail.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """ Process edit user profile """

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect(url_for('homepage'))

    user = User.query.get_or_404(user_id)
    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        if not form.image_url.data:
            form.image_url.data = DEFAULT_IMG_URL
        form.populate_obj(user)

        db.session.commit()
        flash(f'Profile edited', 'success')
        return redirect(url_for('show_user_profile', user_id=user_id))

    return render_template('profile/edit-form.html', form=form)

#######################################
# likes


@app.get('/api/likes')
def check_like():
    """ Given stop id does user like stop
        Return JSON: {"likes": true|false}
    """

    if not g.user:
        return jsonify({'error': 'Not logged in'}), 401

    stop_id = int(request.args.get('stop_id'))
    stop = Stop.query.get_or_404(stop_id)

    if stop in g.user.liked_stops:
        return jsonify({
            'likes': 'true'
        })
    else:
        return jsonify({
            'likes': 'false'
        })


@app.post('/api/like')
def user_likes_stop():
    """ Given stop id, make current user like stop
        Return JSON {"liked": 1}
    """

    if not g.user:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    stop_id = int(data.get('stop_id'))
    stop = Stop.query.get_or_404(stop_id)

    g.user.liked_stops.append(stop)
    db.session.commit()

    return jsonify({"liked": stop_id}), 201


@app.post('/api/unlike')
def user_unlike_stop():
    """Given stop id, make current user unlike stop
        Return JSON {"unliked": 1}
    """

    if not g.user:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    stop_id = int(data.get('stop_id'))
    stop = Stop.query.get_or_404(stop_id)

    g.user.liked_stops.remove(stop)
    db.session.commit()

    return jsonify({"unliked": stop_id}), 201
