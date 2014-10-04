# coding=utf-8

#
# Technical configuration
#
DEBUG = True
ASSETS_DEBUG = DEBUG
SECRET_KEY = "CHANGEME"
# FIXME later
#ASSETS_DEBUG = True
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = '../pages'
SQLALCHEMY_DATABASE_URI = "sqlite:///../data/abilian.db"
SQLALCHEMY_ECHO = False

BROKER_URL = "sqla+" + SQLALCHEMY_DATABASE_URI
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = SQLALCHEMY_DATABASE_URI

SUPER_USERS = ['sf@fermigier.com']

#
# Application configuration
#
SITE_URL = 'http://www.openworldforum.org/'
SITE_TITLE = 'Open World Forum 2014'
SITE_DESCRIPTION = "TODO"

ABSTRACT_LENGTH = 350

FEED_MAX_LINKS = 25
SECTION_MAX_LINKS = 12

ALLOWED_LANGS = ['fr', 'en']

MAIN_MENU = {'fr': [('', u'Accueil'),
                    #('cfp/', u'Contribuez'),
                    ('a-propos/', u'A propos'),
                    ('speakers/', u"Orateurs"),
                    ('schedule/', u'Programme'),
                    ('infos-pratiques/', u'Venir'),
                    #('espace-expo/', u'Exposition'),
                    ('partners/', u'Partenaires'),
                    ('participants/', u'Participants'),
                    #('news/', u'Actualités'),
                    ('/auth/', u'Inscription', 'menu-registration'),
             ],
             'en': [('', u'Home'),
                    #('cfp/', u'CFP'),
                    ('about/', u'About'),
                    ('speakers/', u"Speakers"),
                    ('schedule/', u'Schedule'),
                    ('practical-information/', u'Venue'),
                    #('exhibiton-area/', u'Exhibition'),
                    ('partners/', u'Partners'),
                    ('participants/', u'Participants'),
                    #('news/', u'News'),
                    ('/auth/', u'Registration', 'menu-registration'),
             ]}

IMAGE_SIZES = {
  'small': (300, 180),
  'large': (620, 348),
}

# Mail settings through Gmail smtp for tests.
# export USE_GMAIL_SMTP_FOR=my.gmail.nick:my_gmail_password

import os

if DEBUG and ('OWF_USE_GMAIL_SMTP' in os.environ):
    gmail_user, gmail_password = os.environ['OWF_USE_GMAIL_SMTP'].split(':')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = gmail_user
    MAIL_PASSWORD = gmail_password

# Settings for Students Demo Cup

if DEBUG and ('OWF_SDC_RECIPIENTS' in os.environ):
    SDC_RECIPIENTS = os.environ.get('OWF_SDC_RECIPIENTS').split(':')
else:
    SDC_RECIPIENTS = ['studentdemocup@openworldforum.org']
