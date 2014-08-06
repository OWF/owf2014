import StringIO
import csv

from flask import make_response, current_app
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user
from abilian.core.extensions import db

from .models import Registration, Track
from website.auth.models import User2


class UserView(ModelView):
  column_list = ['email', 'first_name', 'last_name', 'confirmed_at']

  def is_accessible(self):
    if current_app.config.get('DEBUG'):
      return True
    return current_user.is_authenticated()

  @expose("/export.csv")
  def csv(self):
    output = StringIO.StringIO()
    writer = csv.writer(output)
    tracks = [t.title for t in Track.query.all()]
    for r in Registration.query.all():
      row = [r.created_at.strftime("%Y/%m/%d"),
             r.confirmed_at,
             r.email.encode("utf8")]
      #for track in tracks:
      #  row.append()

      writer.writerow(row)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/csv'
    return response


class TrackView(ModelView):
  column_list = ['day', 'theme', 'title']

  def is_accessible(self):
    if current_app.config.get('DEBUG'):
      return True
    return current_user.is_authenticated()

  @expose("/export.csv")
  def csv(self):
    output = StringIO.StringIO()
    writer = csv.writer(output)
    for t in Track.query.all():
      participants = t.participants
      confirmed_participants = [p for p in participants if p.confirmed_at]
      row = [t.theme, t.title.encode("utf8"), len(confirmed_participants), len(participants)]

      writer.writerow(row)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/csv'
    return response


def register_plugin(app):
  admin = app.extensions['admin'][0]
  admin.add_view(UserView(User2, db.session))
  admin.add_view(TrackView(Track, db.session))

