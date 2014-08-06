
import json
import requests
from flask import request, session, abort

from . import route
from .models import User2, db


@route('/persona/login', methods=['POST'])
def persona_login():
  # The request has to have an assertion for us to verify
  if 'assertion' not in request.form:
    abort(400)

  # Send the assertion to Mozilla's verifier service.
  data = {'assertion': request.form['assertion'],
          'audience': request.host_url}
  resp = requests.post('https://verifier.login.persona.org/verify',
                       data=data, verify=True)

  # Did the verifier respond?
  if resp.ok:
    # Parse the response
    verification_data = json.loads(resp.content)

    # Check if the assertion was valid
    if verification_data['status'] == 'okay':
      email = verification_data['email']
      user = get_or_create_user(email)
      # Log the user in by setting a secure session cookie
      session['user_id'] = user.id
      session['auth_provider'] = 'persona'
      return 'You are logged in'

  # Oops, something failed. Abort.
  abort(500)


@route('/persona/logout', methods=['POST'])
def persona_logout():
  """This is what persona.js will call to sign the user out again.
  """
  if 'user_id' in session:
    del session['user_id']
  return 'OK'


def get_or_create_user(email):
  user = User2.query.filter(User2.email == email).first()
  if not user:
    user = User2(email=email)
    db.session.add(user)
    db.session.commit()
  return user
