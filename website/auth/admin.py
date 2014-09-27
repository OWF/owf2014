import StringIO
import csv

from flask import current_app, make_response
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from marshmallow import Serializer

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

    headers = [k for k in UserSerializer.Meta.fields]
    writer.writerow(headers)

    for user in User2.query.all():
      d = UserSerializer(user).data
      def encode(x):
        if isinstance(x, unicode):
          return x.encode('utf8')
        else:
          return str(x)
      row = [encode(d[k]) for k in headers]
      writer.writerow(row)

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/csv'
    return response


def register_admin_views(app):
  admin = app.extensions['admin'][0]
  admin.add_view(UserModelView(User2, db.session))
  admin.add_view(SecureModelView(Role, db.session))


class UserSerializer(Serializer):
  class Meta:
    fields = ['confirmed_at', 'email', 'first_name', 'last_name', 'gender',
              'title', 'organization', 'organization_type', 'url']
