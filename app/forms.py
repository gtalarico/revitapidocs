from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email

class LoginForm(Form):
    email = TextField('email', validators=[Required(), Email('Email is invalid.')])
    password = PasswordField('password', validators=[Required('Password is invalid.')])
    remember_me = BooleanField('remember_me', default=False)

class CreateAccountForm(Form):
    firstname = TextField('firstname', validators=[Required()])
    lastname = TextField('lastname', validators=[Required()])
    email = TextField('email', validators=[Required(), Email()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class EditUserForm(Form):
    firstname = TextField('firstname', validators=[Required()])
    lastname = TextField('lastname', validators=[Required()])
