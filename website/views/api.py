from flask import Blueprint, jsonify
from website.crm.models import Talk, Speaker


blueprint = Blueprint('api', __name__, url_prefix='/api')
route = blueprint.route


#
# API
#
@route('/talks')
def talks():
  all_talks = Talk.query.filter(Talk.starts_at != None).order_by(
    Talk.starts_at).all()

  def isoformat(d):
    if d:
      return d.isoformat()
    else:
      return None

  all_talks = [
    {'id': talk.id,
     'title': talk.title,
     'abstract': talk.abstract,
     'theme': talk.track.theme,
     'track': talk.track.name,
     'room': talk.track.room.name,
     'starts_at': isoformat(talk.starts_at),
     'ends_at': isoformat(talk.ends_at),
     'duration': talk.duration,
     'speakers': [speaker.id for speaker in talk.speakers],
    } for talk in all_talks
  ]
  return jsonify(talks=all_talks)


@route('speakers')
def speakers():
  all_speakers = Speaker.query.all()
  all_speakers = [
    {'id': speaker.id,
     'name': speaker.name,
     'bio': speaker.bio,
     'organisation': speaker.organisation,
     'website': speaker.website,
     'talks': [talk.id for talk in speaker.talks],
    } for speaker in all_speakers
  ]
  return jsonify(speakers=all_speakers)


def register(app):
  app.register_blueprint(blueprint)
