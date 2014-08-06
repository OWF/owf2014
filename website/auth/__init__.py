from flask import Blueprint, session, g, request, url_for
from flask.ext.security import Security, AnonymousUser
from werkzeug.exceptions import HTTPException

from .admin import register_admin_views
from .models import User2, db


security = Security()

blueprint = Blueprint('auth', __name__, template_folder='templates',
                      url_prefix='/auth')
route = blueprint.route

__all__ = ['route', 'register_plugin']


class HTTPRedirectException(HTTPException):
  code = 302

  def __init__(self, location):
    HTTPException.__init__(self)
    self.location = location

  def get_headers(self, environ):
    headers = HTTPException.get_headers(self, environ)
    headers.append(['Location', self.location])
    return headers


def retrieve_user():
  g.user = AnonymousUser()
  user_id = session.get('user_id')
  if user_id:
    g.user = User2.query.get(user_id)
    return

  if 'user_email' in session:
    email = session['user_email']
  else:
    email = None

  if not email:
    return

  if email:
    user = User2.query.filter(User2.email == email).first()
    if not user:
      user = User2(email=email)
      db.session.add(user)
      db.session.commit()
    g.user = user
    session['user_id'] = user.id

  if not g.user.registered and request.path != "/auth/edit_profile":
    raise HTTPRedirectException("/auth/edit_profile")



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
