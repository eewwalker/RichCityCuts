"""Forms for Rich City Stops"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, Optional, URL, Length


class StopAddEditForm(FlaskForm):
    """ Form for adding and editing stop """
    name = TextAreaField(
        'Name',
        validators=[InputRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=[InputRequired()]
    )
    url = TextAreaField(
        'URL(optional)',
        validators=[Optional(), URL()]
    )
    address = TextAreaField(
        'Address',
        validators=[InputRequired()]
    )
    hood_code = SelectField(
        'Neighborhood',
        choices=[]
    )
    image_url = TextAreaField(
        'Image(optional)',
        validators=[Optional(), URL()]
    )


class SignUpForm(FlaskForm):
    """ Form for signing up new user"""
    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)]
    )
    first_name = StringField(
        'First name',
        validators=[InputRequired(), Length(max=30)]
    )
    last_name = StringField(
        'Last name',
        validators=[InputRequired(), Length(max=30)]
    )
    description = TextAreaField(
        'About yourself(optional)',
        validators=[Optional()]
    )
    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=5, max=55)]
    )
    image_url = TextAreaField(
        'Profile Picture URL(optional)',
        validators=[Optional(), URL()]
    )


class LoginForm(FlaskForm):
    """ Login form"""
    username = StringField(
        'Username',
        validators=[InputRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )


class CSRFProtectionForm(FlaskForm):
    """ CSRF Protection Form """


class ProfileEditForm(FlaskForm):
    """ Form to Edit User Information """

    first_name = StringField(
        'First name',
        validators=[Length(max=30)]
    )
    last_name = StringField(
        'Last name',
        validators=[Length(max=30)]
    )
    description = TextAreaField(
        'About yourself(optional)',
        validators=[Optional()]
    )
    email = StringField(
        'E-mail',
        validators=[Email(), Length(max=50)]
    )
    image_url = TextAreaField(
        'Profile Picture URL(optional)',
        validators=[Optional(), URL()]
    )
