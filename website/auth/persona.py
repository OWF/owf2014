import json
import requests
from flask import request, session, abort

from . import route


@route('/persona/login', methods=['POST'])
def persona_login():
  # The request has to have an assertion for us to verify
  if 'assertion' not in request.form:
    abort(400)

  # Send the assertion to Mozilla's verifier service.
  data = {'assertion': request.form['assertion'],
          'audience': request.host_url}
  print session
  resp = requests.post('https://verifier.login.persona.org/verify',
                       data=data, verify=True)

  # Did the verifier respond?
  if resp.ok:
    # Parse the response
    verification_data = json.loads(resp.content)

    # Check if the assertion was valid
    if verification_data['status'] == 'okay':
      # Log the user in by setting a secure session cookie
      session.update({'user_email': verification_data['email']})
      return 'You are logged in'

  # Oops, something failed. Abort.
  abort(500)


@route('/persona/logout', methods=['POST'])
def persona_logout():
  """This is what persona.js will call to sign the user out again.
  """
  print session
  session.clear()
  return 'OK'