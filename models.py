"""Data models for Rich City Stops"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """"User for app"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String(30),
        nullable=True,
        unique=True
    )

    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default='/static/images/rosie.jpg'
    )

    hashed_password = db.Column(
        db.Text,
        nullable=False
    )

    @classmethod
    def get_full_name(cls):
        """ Return full name of user """
        return f'{cls.first_name} {cls.last_name}'

    @classmethod
    def register(cls, username, email, first_name, last_name, description, image_url, password):
        """ Register new user and handle password hashing"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            image_url=image_url,
            hashed_password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenicate(cls, username, password):
        """ Authenicate user to site. Return user instance or False"""

        user = User.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Neighborhood(db.Model):
    """Neighborhood for stop."""

    __tablename__ = 'neighborhoods'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )


class Stop(db.Model):
    """Stops information."""

    __tablename__ = 'stops'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    hood_code = db.Column(
        db.Text,
        db.ForeignKey('neighborhoods.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/richmond.jpeg",

    )

    neighborhood = db.relationship("Neighborhood", backref='stops')

    def __repr__(self):
        return f'<Neighborhood id={self.id} name="{self.name}">'


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
