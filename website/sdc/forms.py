# -*- coding: utf-8 -*-
"""
=========
sdc.forms
=========

Form definition
"""

from wtforms import StringField, SelectField

from flask.ext.wtf import Form, TextAreaField, required, email
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _l

from .common import THEMES_AS_CHOICE

__all__ = ['SDCApplicationForm']


class SDCApplicationForm(Form):
    theme = SelectField(u"Merci de choisir une catégorie", choices=THEMES_AS_CHOICE, validators=[required()])
    leader = StringField(u"Votre nom", validators=[required()])
    prenom = StringField(u"Votre prénom", validators=[required()])
    email = EmailField(u"Your email address", validators=[required(), email()])
    telephone = StringField(u"Votre téléphone", validators=[required()])
    organization = StringField(u"Etablissement / entreprise", validators=[required()])
    intervenants = TextAreaField(u"Autres intervenants (autant de possible)")
    summary = TextAreaField(u"Résumé du projet", validators=[required()])
