"""Data models for Rich City Stops"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
DEFAULT_IMG_URL = 'https://i.etsystatic.com/16944493/r/il/4f0938/3037341557/il_1588xN.3037341557_8qcl.jpg'
DEFAULT_STOP_URL = 'https://www.nps.gov/subjects/urban/images/richmond.PNG'
from mapping import save_map

bcrypt = Bcrypt()
db = SQLAlchemy()


class Like(db.Model):
    """ A through table to connect users and stops """
    __tablename__ = 'likes'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        primary_key=True
    )
    stop_id = db.Column(
        db.Integer,
        db.ForeignKey('stops.id'),
        nullable=False,
        primary_key=True
    )


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
        default=DEFAULT_IMG_URL
    )

    hashed_password = db.Column(
        db.Text,
        nullable=False
    )

    liked_stops = db.relationship(
        'Stop', secondary='likes', backref='liking_users')

    def get_full_name(self):
        """ Return full name of user """
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def register(
        cls,
        username,
        first_name,
        last_name,
        description,
        email,
        password,
        image_url='/static/images/rosie.jpg',
        admin=False
    ):
        """ Register new user and handle password hashing"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            image_url=image_url,
            hashed_password=hashed_pwd,
            admin=admin
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """ Authenicate user to site. Return user instance or False"""

        user = User.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(
                user.hashed_password, password)
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
        default=DEFAULT_STOP_URL

    )

    def save_map(self):
        return save_map(self.id, self.address)

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
