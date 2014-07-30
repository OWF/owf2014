from flask import Blueprint, request, url_for, session, jsonify
from flask.ext.oauthlib.client import OAuth


blueprint = Blueprint('auth', __name__, template_folder='templates',
                      url_prefix='/auth')
route = blueprint.route

__all__ = ['route', 'register_plugin']


#
# Register blueprint on app
#
def register_plugin(app):
  from .oauth import oauth
  from . import persona

  oauth.init_app(app)
  app.register_blueprint(blueprint)
