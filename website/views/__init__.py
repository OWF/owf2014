#
# Register blueprints on app
#
def register_plugin(app):
  from .localized import register
  register(app)

  from .main import register
  register(app)

  from .redirects import register
  register(app)

  from .metadata import register
  register(app)
