# -*- coding: utf-8 -*-
"""
=========
sdc.views
=========


"""

from itsdangerous import URLSafeSerializer
from datetime import datetime
from markupsafe import Markup
from flask import g, Blueprint, render_template, request, flash, redirect, \
    url_for, current_app as app, session
from flask.ext.babel import lazy_gettext as _l, gettext as _
from flask.ext.mail import Message

from abilian.core.extensions import db, mail

from .forms import SDCApplicationForm
from .models import SDCApplication


__all__ = ['sdc']

sdc = Blueprint('sdc', __name__, template_folder='templates',
                url_prefix='/sdc')

route = sdc.route


@route('/', methods=['GET'])
def display_form():
    form = SDCApplicationForm()
    page = dict(title=_l(u"Candidature pour la Student Demo Cup"))
    return render_template("sdc/form.html", page=page, form=form)


@route('/', methods=['POST'])
def submit_form():
    if request.form['_action'] == 'cancel':
        return redirect("/")
    form = SDCApplicationForm(request.form)
    if form.validate():
        application = SDCApplication()
        form.populate_obj(application)
        send_application_by_email(application)
        db.session.add(application)
        db.session.commit()
        msg = Markup(
            "Merci pour votre participation. <a href='/'>Back to the home page.</a>")
        flash(msg, "success")
        return redirect(url_for(".display_form"))

    else:
        page = dict(title="Apply the ")
        return render_template("sdc/form.html", page=page, form=form)


def send_application_by_email(application):
    recipients = app.config.get('SDC_RECIPIENTS')
    body = render_template("sdc/email.txt", proposal=application)
    msg = Message("New application to the student demo cup",
                  body=body,
                  sender="robot@openworldforum.org",
                  recipients=recipients)
    mail.send(msg)
