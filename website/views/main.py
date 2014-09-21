"""
Main view (mostly technical views like sitemap or images).
"""

from cStringIO import StringIO
import mimetypes
import os
from os.path import join
from tempfile import mktemp
import traceback
from PIL import Image
import datetime
from abilian.core.extensions import db
from icalendar import Calendar, Event

from flask import Blueprint, redirect, url_for, request, abort, make_response, \
  render_template, current_app as app, session, jsonify, json, g

from ..content import get_pages
from website.crm.models import Talk, Speaker, Track2
from website.excel import Loader
from website.util import preferred_language
from werkzeug.routing import RequestRedirect


__all__ = ['setup']

main = Blueprint('main', __name__, url_prefix='/')


def register(app):
  app.register_blueprint(main)


#
# Global (app-level) routes
#
@main.route('')
def index():
  lang = session.get('lang')
  if not lang:
    lang = preferred_language()
  if lang == 'fr':
    return redirect(url_for("localized.home", lang='fr'))
  else:
    return redirect(url_for("localized.home", lang='en'))


@main.route('robots.txt')
def robots_txt():
  return ""


@main.route('image/<path:path>')
def image(path):
  hsize = int(request.args.get("h", 0))
  vsize = int(request.args.get("v", 0))

  if hsize > 1000 or vsize > 1000:
    abort(500)

  if '..' in path:
    abort(500)
  fd = open(join(app.root_path, "images", path))
  data = fd.read()

  if hsize:
    image = Image.open(StringIO(data))
    x, y = image.size

    x1 = hsize
    y1 = int(1.0 * y * hsize / x)
    image.thumbnail((x1, y1), Image.ANTIALIAS)
    output = StringIO()
    image.save(output, "PNG")
    data = output.getvalue()
  if vsize:
    image = Image.open(StringIO(data))
    x, y = image.size

    x1 = int(1.0 * x * vsize / y)
    y1 = vsize
    image.thumbnail((x1, y1), Image.ANTIALIAS)
    output = StringIO()
    image.save(output, "PNG")
    data = output.getvalue()

  response = make_response(data)
  response.headers['content-type'] = mimetypes.guess_type(path)[0]
  return response


@main.route('feed/')
def global_feed():
  return redirect("/en/feed/", 301)


@main.route('sitemap.xml')
def sitemap_xml():
  today = datetime.date.today()
  recently = datetime.date(year=today.year, month=today.month, day=1)
  response = make_response(render_template('sitemap.xml', pages=get_pages(),
                                           today=today, recently=recently))
  response.headers['Content-Type'] = 'text/xml'
  return response


#
# API
#
@main.route('api/talks')
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


@main.route('api/speakers')
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


@main.route('ical/talks.ics')
def talks_ics():
  cal = Calendar()
  cal.add('prodid', '-//Open World Forum//openworldforum.org//')
  cal.add('version', '2.0')
  for talk in Talk.query.all():
    if talk.starts_at:
      event = Event()
      event.add('summary', talk.title)
      event.add('dtstart', talk.starts_at)
      event.add('dtend', talk.ends_at)
      event.add('dtstamp', talk.starts_at)
      event['uid'] = 'talk-%d@openworkforum.org' % talk.id
      event.add('priority', 5)
      cal.add_component(event)

  result = StringIO()
  result.write(cal.to_ical())
  response = make_response(result.getvalue())
  response.headers['content-type'] = 'text/calendar'
  return response


@main.route('ical/tracks.ics')
def tracks_ics():
  cal = Calendar()
  cal.add('prodid', '-//Open World Forum//openworldforum.org//')
  cal.add('version', '2.0')
  for track in Track2.query.all():
    if track.starts_at:
      event = Event()
      event.add('summary', track.name)
      event.add('dtstart', track.starts_at)
      event.add('dtend', track.ends_at)
      event.add('dtstamp', track.starts_at)
      event['uid'] = 'track-%d@openworkforum.org' % track.id
      event.add('priority', 5)
      cal.add_component(event)

  result = StringIO()
  result.write(cal.to_ical())
  response = make_response(result.getvalue())
  response.headers['content-type'] = 'text/calendar'
  return response


@main.route("lanyrd.json")
def lanyrd():
  g.lang = 'en'
  talks_list = []
  for talk in Talk.query.all():
    talk_d = {}
    talk_d["crowdsource_ref"] = "org.openworldforum/talks/{}".format(talk.id)
    talk_d["title"] = talk.title
    talk_d['abstract'] = talk.abstract
    talk_d['space_name'] = talk.track.room.name
    talk_d['venue'] = "vcxfq"
    talk_d['start_time'] = talk.starts_at.strftime("%Y-%m-%d %H:%M:%S")
    talk_d['end_time'] = talk.ends_at.strftime("%Y-%m-%d %H:%M:%S")
    talk_d['speakers'] = [
      {'crowdsource_ref': "org.openworldforum/speakers/{}".format(speaker.id),
       'name': speaker.name,
       'role': u"{}, {}".format(speaker.title or "Unknown",
                                speaker.organisation),
       'bio': speaker.bio}
      for speaker in talk.speakers
    ]
    talks_list.append(talk_d)
  data = json.dumps(talks_list, indent=2)
  response = make_response(data)
  response.headers['Content-Type'] = 'application/json'
  return response


@main.route("upload_excel_file", methods=['PUT'])
def upload_excel_file():
  fn = mktemp()
  print fn
  fd = open(fn, "wc")
  fd.write(request.stream.read())
  fd.flush()
  loader = Loader(fn)
  try:
    loader.load()
    db.session.commit()
    os.unlink(fn)
    return 'OK\n'
  except:
    os.unlink(fn)
    return "\n".join(loader.log) + "\n" + traceback.format_exc()

