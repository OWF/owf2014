from flask import request, url_for, session, jsonify, render_template, redirect, \
  g, flash
from flask.ext.oauthlib.client import OAuth, OAuthException
from flask.ext.babel import lazy_gettext as _l, gettext as _

from . import route
from .models import User2, db


oauth = OAuth()

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1.1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           app_key="TWITTER")

github = oauth.remote_app('github',
                          base_url='https://api.github.com/',
                          request_token_params={'scope': 'user:email'},
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://github.com/login/oauth/access_token',
                          authorize_url='https://github.com/login/oauth/authorize',
                          app_key='GITHUB')

linkedin = oauth.remote_app('linkedin',
                            base_url='https://api.linkedin.com/v1/',
                            request_token_params={
                              'scope': 'r_basicprofile',
                              'state': 'RandomString',
                            },
                            request_token_url=None,
                            access_token_method='POST',
                            access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
                            authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
                            app_key='LINKEDIN')

google = oauth.remote_app('google',
                          base_url='https://www.googleapis.com/oauth2/v1/',
                          request_token_params={
                            'scope': 'https://www.googleapis.com/auth/userinfo.email'
                          },
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          app_key='GOOGLE')

facebook = oauth.remote_app('facebook',
                            request_token_params={'scope': 'email'},
                            base_url='https://graph.facebook.com',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            app_key='FACEBOOK')

xing = oauth.remote_app('xing',
                        base_url="https://api.xing.com/v1/",
                        request_token_url="https://api.xing.com/v1/request_token",
                        access_token_method='POST',
                        access_token_url='https://api.xing.com/v1/access_token',
                        authorize_url='https://api.xing.com/v1/authorize',
                        app_key='XING')

stackoverflow = oauth.remote_app('stackoverflow',
                                 base_url="https://api.stackexchange.com/2.1/",
                                 request_token_url=None,
                                 access_token_method='POST',
                                 access_token_url='https://stackexchange.com/oauth/access_token',
                                 authorize_url='https://stackexchange.com/oauth',
                                 app_key='STACKOVERFLOW')

linuxfr = oauth.remote_app('linuxfr',
                           base_url="https://api.stackexchange.com/2.1/",
                           request_token_url=None,
                           access_token_method='POST',
                           access_token_url='https://linuxfr.org/auth/oauth/access_token',
                           authorize_url='https://linuxfr.org/auth/oauth/authorize',
                           app_key='LINUXFR')

servers = {
  'twitter': twitter,
  'facebook': facebook,
  'github': github,
  'linkedin': linkedin,
  'google': google,
  'xing': xing,
  'stackoverflow': stackoverflow,
  'linuxfr': linuxfr,
}



#
# Views
#
@route('/login/<server_name>')
def login_with(server_name):
  server = servers[server_name]
  url = url_for('.authorized_{}'.format(server_name), _external=True)
  return server.authorize(callback=url)


@route("/")
def login():
  next_url = request.args.get('next') or request.referrer or None
  if next_url and not "/auth/" in next_url:
    session['next_url'] = next_url
  if g.user.is_anonymous():
    return render_template("auth/login.html", title="Login")
  else:
    return redirect(url_for(".profile"))


@route("/logout", methods=['GET', 'POST'])
def logout():
  if g.user.is_anonymous():
    return redirect(url_for(".login"))

  if request.method == 'GET':
    return render_template("auth/logout.html", title="Logout")

  if 'user_id' in session:
    del session['user_id']
  if 'user_email' in session:
    del session['user_email']
  return redirect(url_for(".login"))


#
#
# Google
#
@route("/authorized_google")
@google.authorized_handler
def authorized_google(resp):
  if resp is None or isinstance(resp, OAuthException):
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )

  access_token = resp['access_token']
  session['oauth_token'] = (access_token, '')

  me = google.get('userinfo')
  email = me.data['email']
  if not me.data['verified_email']:
    msg = _(u"Your email needs to be verified with your identity provider.")
    flash(msg, "danger")
    return redirect(".login")

  user = User2.query.filter(User2.email == email).first()
  if not user:
    user = User2(email=email)
    db.session.add(user)

  user.auth_provider = "google"
  user.oauth_id = me.data['id']
  user.google_id = user.oauth_id
  user.access_token = access_token
  user.first_name = me.data['given_name']
  user.last_name = me.data['family_name']
  user.gender = me.data.get('gender', u"")
  user.picture_url = me.data['picture']
  db.session.commit()

  flash(_(u"Login successful."), "success")
  session['user_id'] = user.id
  session['auth_provider'] = 'google'
  next_url = session.get('next_url')
  if next_url:
    del session['next_url']
  return redirect(next_url or "/")


#
# Facebook
#
@route('/authorized_facebook')
@facebook.authorized_handler
def authorized_facebook(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  if isinstance(resp, OAuthException):
    return 'Access denied: %s' % resp.message

  access_token = resp['access_token']
  session['oauth_token'] = (access_token, '')

  me = facebook.get('/me')

  email = me.data['email']
  if not me.data['verified']:
    msg = _(u"Your email needs to be verified with your identity provider.")
    flash(msg, "danger")
    return redirect(".login")

  user = User2.query.filter(User2.email == email).first()
  if not user:
    user = User2(email=email)
    db.session.add(user)

  user.auth_provider = "facebook"
  user.oauth_id = me.data['id']
  user.access_token = access_token
  user.first_name = me.data['first_name']
  user.last_name = me.data['last_name']
  user.gender = me.data['gender']
  db.session.commit()

  flash(_(u"Login successful."), "success")
  session['user_id'] = user.id
  session['auth_provider'] = 'facebook'
  next_url = session.get('next_url')
  if next_url:
    del session['next_url']
  return redirect(next_url or "/")


#
# Github
#
@route("/authorized_github")
@github.authorized_handler
def authorized_github(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )

  access_token = resp['access_token']
  session['oauth_token'] = (access_token, '')

  me = github.get('user')
  data = me.data

  email = data['email']
  user = User2.query.filter(User2.email == email).first()
  if not user:
    user = User2(email=email)
    db.session.add(user)

  user.auth_provider = "github"
  user.oauth_id = data['id']
  user.access_token = access_token
  try:
    user.first_name, user.last_name = data['name'].split(" ", 2)
  except:
    pass
  user.url = data['blog']
  user.picture_url = data['avatar_url']
  user.github_handle = data['login']
  user.organization = data['company'] or u""
  db.session.commit()

  flash(_(u"Login successful."), "success")
  session['user_id'] = user.id
  session['auth_provider'] = 'github'
  next_url = session.get('next_url')
  if next_url:
    del session['next_url']
  return redirect(next_url or "/")


#
# Linuxfr
#
@route("/authorized_linuxfr")
@linuxfr.authorized_handler
def authorized_linuxfr(resp):
  if resp is None:
    return 'Access denied'

  access_token = resp['access_token']
  session['oauth_token'] = (access_token, '')

  me = linuxfr.get('user')

  email = me.data['email']
  user = User2.query.filter(User2.email == email).first()
  if not user:
    user = User2(email=email)
    db.session.add(user)

  user.auth_provider = "linuxfr"
  user.oauth_id = me.data['login']
  user.access_token = access_token
  # user.linuxfr_login = me.data['login']
  db.session.commit()

  flash(_(u"Login successful."), "success")
  session['user_id'] = user.id
  session['auth_provider'] = 'linuxfr'
  next_url = session.get('next_url')
  if next_url:
    del session['next_url']
  return redirect(next_url or "/")


#
# These ones are currently not working or not used
#
@route("/authorized_twitter")
@twitter.authorized_handler
def authorized_twitter(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = resp
  me = twitter.get('account/verify_credentials.json')
  return jsonify({"data": me.data})


@route("/authorized_linkedin")
@linkedin.authorized_handler
def authorized_linkedin(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = (resp['access_token'], '')
  me = linkedin.get('people/~')
  return jsonify({"data": me.data})


def change_linkedin_query(uri, headers, body):
  auth = headers.pop('Authorization')
  headers['x-li-format'] = 'json'
  if auth:
    auth = auth.replace('Bearer', '').strip()
    if '?' in uri:
      uri += '&oauth2_access_token=' + auth
    else:
      uri += '?oauth2_access_token=' + auth
  return uri, headers, body


linkedin.pre_request = change_linkedin_query


@route("/authorized_stackoverflow")
@stackoverflow.authorized_handler
def authorized_stackoverflow(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = (resp['access_token'], '')
  me = linkedin.get('people/~')
  return jsonify({"data": me.data})


@route("/authorized_xing")
@xing.authorized_handler
def authorized_xing(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = (resp['oauth_token'], '')
  me = google.get('userinfo')
  return jsonify({"data": me.data})


def get_oauth_token():
  return session.get('oauth_token')


for app in servers.values():
  app.tokengetter(get_oauth_token)