from flask import current_app
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


def register_admin_views(app):
  admin = app.extensions['admin'][0]
  admin.add_view(SecureModelView(User2, db.session))
  admin.add_view(SecureModelView(Role, db.session))
