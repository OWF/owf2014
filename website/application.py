# coding=utf-8

import locale
from os import mkdir
from os.path import join, dirname, exists
import re

from flask import Flask, abort, request, g, session, redirect
from flask.ext.admin import Admin
from flask.ext.bootstrap import Bootstrap
from flask.ext.frozen import Freezer
from flask.ext.flatpages import FlatPages
from flask.ext.markdown import Markdown
from flask.ext.assets import Environment as AssetManager
from flask.ext.login import current_user

import abilian
from abilian.i18n import babel
from abilian.app import PluginManager, ServiceManager
from abilian.core.extensions import db, mail
from abilian.web.filters import init_filters

from .util import preferred_language
from .whoosh import Whoosh
from . import linuxipsum


__all__ = ['create_app', 'create_db']


class Application(Flask, PluginManager, ServiceManager):
  def __init__(self, name=None, config=None, *args, **kwargs):
    Flask.__init__(self, name, *args, **kwargs)
    ServiceManager.__init__(self)
    PluginManager.__init__(self)


def create_app(config=None):
  app = Application(__name__, instance_relative_config=True)
  if not config:
    from . import config
    #app.config.from_pyfile('secrets.cfg', silent=True)
    app.config.from_pyfile('secrets.cfg')
  app.config.from_object(config)
  setup(app)
  return app


#
# Setup helpers
#
def setup(app):
  db.init_app(app)
  mail.init_app(app)
  #login_manager.init_app(app)

  admin = Admin(app)
  bootstrap = Bootstrap(app)

  app.register_plugin("website.auth")
  setup_filters_and_processors(app)

  app.register_plugin("website.views")
  #app.register_plugin("website.cfp")
  #app.register_plugin("website.registration")
  app.register_plugin("website.crm")
  app.register_plugin("website.sdc")  # Students demo cup

  # Add some extensions
  whoosh = Whoosh(app)

  pages = FlatPages(app)
  app.extensions['pages'] = pages

  setup_freezer(app)
  markdown_manager = Markdown(app)
  asset_manager = AssetManager(app)
  app.extensions['asset_manager'] = asset_manager

  # Setup custome babel config (see below)
  setup_babel(app)

  # Setup hierarchical Jinja2 template loader
  # TODO: should be generic
  setup_template_loader(app)

  create_db(app)
  load_tracks(app)

  if not app.config.get('TESTING'):
    pass
    #audit_service.init_app(app)
    #audit_service.start()
    #index_service.init_app(app)
    #index_service.start()
    #activity_service.init_app(app)
    #activity_service.start()


def setup_babel(app):
  """
  Setup custom Babel config.
  """
  babel.init_app(app)

  def get_locale():
    lang = getattr(g, 'lang')
    if not lang:
      lang = session.get('lang')
    if not lang:
      lang = preferred_language()
    return lang

  babel.add_translations('website')
  babel.localeselector(get_locale)
  #babel.timezoneselector(get_timezone)


def setup_template_loader(app):
  """
  Not really a hack. Makes possible to get templates from several different
  directories, i.e. useful to override template from a library.
  """
  from jinja2 import ChoiceLoader, FileSystemLoader

  abilian_template_dir = join(dirname(abilian.__file__), "templates")
  my_loader = ChoiceLoader([app.jinja_loader,
                            FileSystemLoader(abilian_template_dir)])
  app.jinja_loader = my_loader


def create_db(app):
  if not exists("data"):
    mkdir("data")

  with app.app_context():
    db.create_all()

    # alembic_ini = join(dirname(__file__), '..', 'alembic.ini')
    # alembic_cfg = flask_alembic.FlaskAlembicConfig(alembic_ini)
    # alembic_cfg.set_main_option('sqlalchemy.url',
    #                             app.config.get('SQLALCHEMY_DATABASE_URI'))
    # alembic.command.stamp(alembic_cfg, "head")

    # if User.query.get(0) is None:
    #   root = User(id=0, last_name=u'SYSTEM', email=u'system@example.com',
    #               can_login=False)
    #   db.session.add(root)
    #   db.session.commit()


def load_tracks(app):
  with app.app_context():
    pass
    # if Track.query.count() == 0:
    #   for track_id, track_title, track_theme, track_day in TRACKS:
    #     track = Track(title=track_title, theme=track_theme, day=track_day)
    #     db.session.add(track)
    #   db.session.commit()


def setup_filters_and_processors(app):
  # Register generic filters from Abilian Core
  init_filters(app)

  @app.template_filter()
  def to_rfc2822(dt):
    if not dt:
      return
    current_locale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
    formatted = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
    locale.setlocale(locale.LC_TIME, current_locale)
    return formatted


  @app.url_defaults
  def add_language_code(endpoint, values):
    if g.lang:
      values.setdefault('lang', g.lang)

  @app.url_value_preprocessor
  def pull_lang(endpoint, values):
    m = re.match("/(..)/", request.path)
    if m:
      g.lang = m.group(1)
    else:
      g.lang = ''
    if g.lang and not g.lang in app.config['ALLOWED_LANGS']:
      abort(404)

  @app.context_processor
  def inject_context():
    return dict(app=app, linuxipsum=linuxipsum.generate)

  @app.before_request
  def before_request():
    if request.path.startswith("/crm"):
      if not current_user.is_authenticated():
        return redirect("/login")

    g.recent_items = []


def setup_freezer(app):
  """FIXME: not used and currently broken."""

  def url_generator():
    # URLs as strings
    yield '/fr/'

  freezer = Freezer(app)
  app.extensions['freezer'] = freezer
  freezer.register_generator(url_generator)
