from flask import Blueprint, jsonify
from markdown import markdown
from marshmallow import Serializer, fields
from sqlalchemy import func
from website.auth import User2

from website.crm.models import Talk, Speaker, Track2


blueprint = Blueprint('api', __name__, url_prefix='/api')
route = blueprint.route


#
# Serializers
#
class TrackSerializer(Serializer):
  id = fields.Integer()
  name = fields.String()
  theme = fields.String()


class TalkSerializer(Serializer):
  id = fields.Integer()
  title = fields.String()

  starts_at = fields.DateTime()
  ends_at = fields.DateTime()
  duration = fields.Integer()

  abstract = fields.Function(lambda obj: markdown(obj.abstract))

  track = fields.Nested(TrackSerializer)
  # TODO: room
  # 'room': talk.track.room.name,

  # noinspection PyTypeChecker
  speakers = fields.Nested('SpeakerSerializer', many=True, only=('id', 'name'))


class SpeakerSerializer(Serializer):
  id = fields.Integer()
  name = fields.String()
  first_name = fields.String()
  last_name = fields.String()
  title = fields.String()
  organisation = fields.String()
  website = fields.String()

  bio = fields.Function(lambda obj: markdown(obj.bio))

  talks = fields.Nested(TalkSerializer, many=True, only=('id', 'title',))


class UserSerializer(Serializer):
  id = fields.Integer()
  name = fields.String()
  first_name = fields.String()
  last_name = fields.String()
  title = fields.String()
  organization = fields.String()
  url = fields.String()
  biography = fields.Function(lambda obj: markdown(obj.biography))


#
# Routes
#
@route('/talks')
def talks():
  talks = Talk.query \
    .filter(Talk.starts_at != None) \
    .order_by(Talk.starts_at).all()

  data = TalkSerializer(talks, many=True).data
  res = jsonify(talks=data)
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res


@route('/talks/<int:id>')
def talk(id):
  talk = Talk.query.get(id)

  data = TalkSerializer(talk).data
  res = jsonify(talk=data)
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res


@route('/speakers')
def speakers():
  speakers = Speaker.query.order_by(func.lower(Speaker.last_name)).all()

  data = SpeakerSerializer(speakers, many=True).data

  res = jsonify(speakers=data)
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res


@route('/speakers/<int:id>')
def speaker(id):
  speaker = Speaker.query.get(id)

  data = SpeakerSerializer(speaker).data
  res = jsonify(speaker=data)
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res


@route('/all')
def all():
  talks = Talk.query \
    .filter(Talk.starts_at != None) \
    .order_by(Talk.starts_at).all()
  serialized_talks = TalkSerializer(talks, many=True).data

  speakers = Speaker.query.order_by(func.lower(Speaker.last_name)).all()
  serialized_speakers = SpeakerSerializer(speakers, many=True).data

  tracks = Track2.query.order_by(Track2.starts_at).all()
  serialized_tracks = TrackSerializer(tracks, many=True).data

  users = User2.query.order_by(User2.last_name, User2.first_name).all()
  serialized_users = UserSerializer(users, many=True).data

  res = jsonify(speaker=serialized_speakers,
                talks=serialized_talks,
                tracks=serialized_tracks,
                users=serialized_users)
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res


def register(app):
  app.register_blueprint(blueprint)


