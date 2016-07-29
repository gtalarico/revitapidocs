from app import db,bcrypt, login_manager
from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

# class User(db.Model, UserMixin):
class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    _password = db.Column(db.String(128))
    authenticated = db.Column(db.Integer)
    email_confirmed = db.Column(db.Integer)
    messages = db.relationship('Message', backref='author', lazy='dynamic')

    def is_email_confirmed(self):
        return self.email_confirmed

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def get_id(self):
        try:
            return unicode(self.uid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __repr__(self):
        return 'User: [{0}]'.format(self.firstname)


class Message(db.Model):
    msgid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))

    def __repr__(self):
        return 'Message: [{0}]'.format(self.body)


#TO DO UNDERSTAND:
#db_create.py
#db_migrate.py
#db_upgrade.py
#db_downgrade.py

# >>> u = models.User(nickname='john', email='john@email.com')
# >>> db.session.add(u)
# >>> db.session.commit()
