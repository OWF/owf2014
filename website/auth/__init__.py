from flask import Blueprint, session, g


blueprint = Blueprint('auth', __name__, template_folder='templates',
                      url_prefix='/auth')
route = blueprint.route

__all__ = ['route', 'register_plugin']


def retrieve_user():
  # g.user = None
  if 'oauth_email' in session:
    g.user_email = session['oauth_email']


#
# Register blueprint on app
#
def register_plugin(app):
  from .oauth import oauth
  from . import persona

  oauth.init_app(app)
  app.register_blueprint(blueprint)
  app.before_request(retrieve_user)
