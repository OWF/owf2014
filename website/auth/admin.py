import StringIO
import csv
from flask import current_app, make_response
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from .models import User2, Role, db


class SecureModelView(ModelView):
  def is_accessible(self):
    super_users = current_app.config['SUPER_USERS']
    if current_user.is_authenticated():
      return current_user.email in super_users
    else:
      return False


class UserModelView(SecureModelView):
  column_list = ('id', 'email', 'first_name', 'last_name', 'organization',
                 'organization_type')


  @expose("/export.csv")
  def csv(self):
    output = StringIO.StringIO()
    writer = csv.writer(output)
    for user in User2.query.all():
      row = [user.confirmed_at.strftime("%Y/%m/%d") if user.confirmed_at else "",
             user.email.encode("utf8"),
             user.first_name.encode("utf8"),
             user.last_name.encode("utf8"),
             user.gender.encode("utf8"),

             user.title.encode("utf8"),
             user.organization.encode("utf8"),
             user.organization_type.encode("utf8"),

             user.url.encode("utf8"),
             user.picture_url.encode("utf8"), ]
      writer.writerow(row)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/csv'
    return response


def register_admin_views(app):
  admin = app.extensions['admin'][0]
  admin.add_view(UserModelView(User2, db.session))
  admin.add_view(SecureModelView(Role, db.session))
