from flask import g, render_template, request, flash, redirect, url_for, session
from flask.ext.babel import lazy_gettext as _l, gettext as _

from ..util import preferred_language

from . import route
from .forms import RegistrationForm
from .models import db


@route('/profile')
def profile():
  return redirect(url_for(".edit_profile"))


@route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
  title = _l(u"Please complete or update your profile")
  page = dict(title=title)

  user = g.user
  if user.is_anonymous():
    return redirect(url_for(".login_screen"))

  if request.method == 'GET':
    form = RegistrationForm(obj=user)
    return render_template("auth/edit_profile.html",
                           page=page, form=form, lang="en")

  action = request.form['_action']
  if action == 'cancel':
    return redirect(url_for(".profile"))

  form = RegistrationForm(request.form)
  if form.validate():
    form.populate_obj(user)
    user.ip_address = request.remote_addr
    user.preferred_lang = preferred_language()
    db.session.commit()

    msg = _(u"Profile edited successfully.")
    flash(msg, "success")

    next_url = session.get('next_url')
    if next_url:
      del session['next_url']
      return redirect(session['next_url'])
    else:
      return redirect(url_for(".profile"))

  else:
    msg = _(u"Please fix the errors belows.")
    flash(msg, "danger")
    return render_template("auth/edit_profile.html",
                           page=page, form=form, lang="en")
