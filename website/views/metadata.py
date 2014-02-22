from flask import g


def prepare_metadata():
  g.metadata = {
    'DC.title': "Open World Forum",
    'DC.publisher': "Open World Forum",
    'og:type': 'website',
    'og:site_name': 'Open World Forum 2014',

    'twitter:site': '@openworldforum',
    'twitter:card': 'summary',
  }


def register(app):
  app.before_request(prepare_metadata)
