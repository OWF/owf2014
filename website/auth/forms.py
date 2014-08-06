from flask.ext.wtf import Form, BooleanField, TextField, TextAreaField, \
  required, email
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _l

from website.registration.models import Track


__all__ = ['RegistrationForm']


class RegistrationForm(Form):
  email = EmailField(label=_l(u"Your email address"),
                     validators=[required(), email()])

  first_name = TextField(label=_l("First name"),
                         validators=[required()])
  last_name = TextField(label=_l("Last name"),
                        validators=[required()])
  title = TextField(label=_l("Title"))

  organization = TextField(label=_l("Organization"),
                           validators=[required()])
  organization_type = TextField(label=_l("Organization type"),
                                validators=[required()])

  url = TextField(label=_l("URL"))
  bio = TextAreaField(label=_l("Biography"))

  # twitter_handle = Column(UnicodeText(100), default="", nullable=False)
  # github_handle = Column(UnicodeText(200), default="", nullable=False)
  # sourceforge_handle = Column(UnicodeText(200), default="", nullable=False)
  # linkedin_url = Column(UnicodeText(200), default="", nullable=False)

