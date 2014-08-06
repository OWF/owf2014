# Define models
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UnicodeText
from flask.ext.security import RoleMixin, UserMixin, SQLAlchemyUserDatastore
from abilian.core.extensions import db
from website.auth.forms import RegistrationForm, UnsecureRegistrationForm

__all__ = ['db', 'Role', 'User2', 'user_datastore']

roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user2.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))


class User2(db.Model, UserMixin):
  __tablename__ = 'user2'
  id = db.Column(Integer, primary_key=True)

  email = Column(String(255), unique=True)

  password = Column(String(255))
  active = Column(Boolean())
  confirmed_at = Column(DateTime())

  auth_provider = Column(String(20))
  oauth_id = Column(String(100))
  access_token = Column(String(100))

  ip_address = Column(String(20))
  preferred_lang = Column(String(5), default='en')

  first_name = Column(UnicodeText(100), default=u"", nullable=False)
  last_name = Column(UnicodeText(100), default=u"", nullable=False)
  gender = Column(UnicodeText(10), default=u"")

  title = Column(UnicodeText(100), default=u"", nullable=False)
  organization = Column(UnicodeText(200), default=u"", nullable=False)
  organization_type = Column(UnicodeText(100), default=u"", nullable=False)

  # TODO
  partners = Column(UnicodeText)

  biography = Column(UnicodeText(2000), default=u"", nullable=False)
  url = Column(UnicodeText(200), default=u"", nullable=False)

  picture_url = String(500)

  google_id = Column(String(200))
  facebook_id = Column(String(200))
  github_id = Column(String(200))

  twitter_handle = Column(UnicodeText(100), default=u"", nullable=False)
  github_handle = Column(UnicodeText(200), default=u"", nullable=False)

  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

  def is_complete(self):
    form = UnsecureRegistrationForm(obj=self)
    return form.validate()

  def __repr__(self):
    return '<User2 {}>'.format(self.email)

  #
  # Aliases
  #
  @property
  def bio(self):
    return self.biography

  @property
  def _name(self):
    return '%s %s' % (self.first_name, self.last_name)

  name = _name



# For Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User2, Role)
