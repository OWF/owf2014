# coding=utf-8
from flask.ext.wtf import Form, TextField, TextAreaField, required
from flask.ext.babel import lazy_gettext as _l
from wtforms import SelectField


__all__ = ['RegistrationForm', 'BaseRegistrationForm']

org_types = [
  u"",
  u"Auto-entrepreneur",
  u"PME",
  u"ETI",
  u"Grand Groupe",
  u"Investisseur",
  u"Académique",
  u"Institutionnel",
  u"Autre",
]
org_types = [(x, x) for x in org_types]


class RegistrationForm(Form):
  first_name = TextField(label=_l("First name"),
                         validators=[required()])
  last_name = TextField(label=_l("Last name"),
                        validators=[required()])
  title = TextField(label=_l("Title"),
                    validators=[required()])

  organization = TextField(label=_l("Organization"),
                           validators=[required()])
  organization_type = SelectField(label=_l("Organization type"),
                                  choices=org_types,
                                  validators=[required()])

  url = TextField(label=_l("URL"))
  biography = TextAreaField(label=_l("Biography"))

  # twitter_handle = Column(UnicodeText(100), default="", nullable=False)
  # github_handle = Column(UnicodeText(200), default="", nullable=False)
  # sourceforge_handle = Column(UnicodeText(200), default="", nullable=False)
  # linkedin_url = Column(UnicodeText(200), default="", nullable=False)


class UnsecureRegistrationForm(RegistrationForm):
  def validate_csrf_token(self, field):
    return
