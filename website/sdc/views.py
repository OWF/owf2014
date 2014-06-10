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
    page = dict(title=_l(u"Apply to the Student Demo Cup"))
    return render_template("sdc/form.html", page=page, form=form)


@route('/', methods=['POST'])
def submit_form():
    if request.form['_action'] == 'cancel':
        return redirect("/")
    form = SDCApplicationForm(request.form)
    if form.validate():
        proposal = SDCApplication()
        form.populate_obj(proposal)
        send_proposal_by_email(proposal)
        db.session.add(proposal)
        db.session.commit()
        msg = Markup(
            "Thank you for your submission. <a href='/'>Back to the home page.</a>")
        flash(msg, "success")
        return redirect(url_for(".display_form"))

    else:
        page = dict(title="Apply the ")
        return render_template("sdc/form.html", page=page, form=form)


def send_proposal_by_email(proposal):
    if app.config.get('TESTING'):
        recipients = ["gilles.lenfant@alterway.fr"]
    else:
        recipients = ["sf@fermigier.com", "program@openworldforum.org"]

    body = render_template("email.txt", proposal=proposal)
    msg = Message("New application to the student demo cup",
                  body=body,
                  sender="robot@openworldforum.org",
                  recipients=recipients)
    mail.send(msg)
