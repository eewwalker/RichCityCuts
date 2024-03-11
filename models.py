"""Data models for Rich City Stops"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


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

    # state = db.Column(
    #     db.String(2),
    #     nullable=False,
    # )


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

    # def get_city_state(self):
    #     """Return 'city, state' for cafe."""

    #     city = self.city
    #     return f'{city.name}, {city.state}'


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
