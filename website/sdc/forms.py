# -*- coding: utf-8 -*-
"""
=========
sdc.forms
=========

Form definition
"""

from flask.ext.wtf.html5 import EmailField
from wtforms import StringField, TextAreaField, RadioField, SelectField

from flask.ext.wtf import Form, BooleanField, TextField, TextAreaField, required, email
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _l

# from website.sdc.models import Registration

from .common import THEMES_AS_CHOICE

__all__ = ['SDCApplicationForm']


class SDCApplicationForm(Form):
    theme = SelectField(label=_l(u"Please choose a theme"), choices=THEMES_AS_CHOICE, validators=[required()])
    leader = StringField(label=_l(u"Your name"), validators=[required()])
    email = EmailField(label=_l(u"Your email address"), validators=[required(), email()])
    organization = StringField(label=_l(u"Your organization"), validators=[required()])
    speakers = StringField(label=_l(u"Other speakers"))
    summary = TextAreaField(label=_l(u"Your project summary"), validators=[required()])
