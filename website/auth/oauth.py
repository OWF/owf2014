from flask import request, url_for, session, jsonify, render_template
from flask.ext.oauthlib.client import OAuth, OAuthException

from . import route


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

servers = {
  'twitter': twitter,
  'facebook': facebook,
  'github': github,
  'linkedin': linkedin,
  'google': google,
  'xing': xing,
  'stackoverflow': stackoverflow,
}



#
# Views
#
@route('/login/<server_name>')
def login(server_name):
  server = servers[server_name]
  next = request.args.get('next') or request.referrer or None
  # url = url_for('.authorized_{}'.format(server_name), next=next,
  #               _external=True)
  url = "http://www.openworldforum.paris/auth/authorized_{}".format(server_name)
  return server.authorize(callback=url)


@route("/")
def login_screen():
  return render_template("auth/login.html", title="Login")


#
# Twitter
#
@route("/authorized_twitter")
@twitter.authorized_handler
def authorized_twitter(resp):
  print resp
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = resp
  me = twitter.get('account/verify_credentials.json')
  return jsonify({"data": me.data})


#
# Google
#
@route("/authorized_google")
@google.authorized_handler
def authorized_google(resp):
  print resp
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = (resp['access_token'], '')
  me = google.get('userinfo')
  return jsonify({"data": me.data})


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

  session['oauth_token'] = (resp['access_token'], '')
  me = facebook.get('/me')
  return 'Logged in as id=%s name=%s redirect=%s' % \
         (me.data['id'], me.data['name'], request.args.get('next'))


#
# Github
#
@route("/authorized_github")
@github.authorized_handler
def authorized_github(resp):
  print resp
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
      request.args['error_reason'],
      request.args['error_description']
    )
  session['oauth_token'] = (resp['access_token'], '')
  me = github.get('user')
  return jsonify({"data": me.data})


#
# Linkedin
#
@route("/authorized_linkedin")
@linkedin.authorized_handler
def authorized_linkedin(resp):
  print resp
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


#
# Stackoverflow
#
@route("/authorized_stackoverflow")
@stackoverflow.authorized_handler
def authorized_stackoverflow(resp):
  print resp
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
  print resp
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