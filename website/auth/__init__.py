from flask import Blueprint, session, g, request
from flask.ext.security import Security, AnonymousUser
from werkzeug.exceptions import HTTPException
from werkzeug.routing import RequestRedirect

from .admin import register_admin_views
from .models import User2, db


security = Security()

blueprint = Blueprint('auth', __name__, template_folder='templates',
                      url_prefix='/auth')
route = blueprint.route

__all__ = ['route', 'register_plugin']


def retrieve_user():
  g.user = AnonymousUser()
  user_id = session.get('user_id')
  if user_id:
    user = User2.query.get(user_id)
    if user:
      g.user = user
    else:
      del session['user_id']

  if g.user.is_anonymous() or request.path.startswith("/static/"):
    return

  if not g.user.is_complete() and not request.path.startswith("/auth/"):
    raise RequestRedirect("/auth/edit_profile")


#
# Register blueprint on app
#
def register_plugin(app):
  from .oauth import oauth
  from . import persona, profile
  from .models import user_datastore

  oauth.init_app(app)
  app.register_blueprint(blueprint)
  app.before_request(retrieve_user)

  security.init_app(app, user_datastore)
  register_admin_views(app)
