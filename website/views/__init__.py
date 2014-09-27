#
# Register blueprints on app
#
def register_plugin(app):
  from . import localized, main, redirects, metadata, api

  localized.register(app)
  main.register(app)
  redirects.register(app)
  metadata.register(app)
  api.register(app)
