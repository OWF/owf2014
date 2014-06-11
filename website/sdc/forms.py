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
    theme = SelectField(label=_l(u"Merci de choisir une catégorie"), choices=THEMES_AS_CHOICE, validators=[required()])
    leader = StringField(label=_l(u"Votre nom"), validators=[required()])
    prenom = StringField(label=_l(u"Votre prénom"), validators=[required()])
    email = EmailField(label=_l(u"Your email address"), validators=[required(), email()])
    telephone = StringField(label=_l(u"Votre téléphone"), validators=[required()])
    organization = StringField(label=_l(u"Etablissement / entreprise"), validators=[required()])
    intervenants = TextAreaField(label=_l(u"Autres intervenants (autant de possible"), validators=[required()])
    summary = TextAreaField(label=_l(u"Résumé du projet"), validators=[required()])

