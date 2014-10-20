"""
Main view (mostly technical views like sitemap or images).
"""

from cStringIO import StringIO
import hashlib
import mimetypes
import os
from os.path import join
import re
from tempfile import mktemp
import traceback
import zipfile
from PIL import Image
import datetime
from abilian.core.extensions import db
from icalendar import Calendar, Event

from flask import Blueprint, redirect, url_for, request, abort, make_response, \
  render_template, current_app as app, session, jsonify, json, g
import requests

from ..content import get_pages
from website.auth import User2
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
  fd = open(fn, "wc")
  fd.write(request.stream.read())
  fd.flush()
  loader = Loader(fn)
  try:
    loader.load()
    db.session.commit()
    log = loader.log
  except:
    log = loader.log + "\n" + traceback.format_exc()
  finally:
    os.unlink(fn)

  fix_speaker_bios()

  return log


def fix_speaker_bios():
  for speaker in Speaker.query.filter().all():
    if speaker.bio_fr or speaker.bio_en:
      continue
    user = User2.query.filter(User2.email == speaker.email).first()
    if not user or not user.biography:
      continue
    speaker.bio_en = user.biography
  db.session.commit()


@main.route("upload_photos", methods=['PUT'])
def upload_photos():
  fn = mktemp()
  fd = open(fn, "wc")
  fd.write(request.stream.read())
  fd.flush()
  zip = zipfile.ZipFile(fn)
  for info in zip.infolist():
    name = info.filename.split("/")[-1].lower()
    m = re.match(r"(.*)\.(jpeg|jpg)", name)
    if not m:
      continue
    email = m.group(1)
    data = zip.read(info.filename)
    speaker = Speaker.query.filter(Speaker.email == email).first()
    if not speaker:
      print "Skipping {}".format(email)
      continue
    speaker.photo = data
    print "Adding picture for {}".format(email)

  db.session.commit()

  for speaker in Speaker.query.filter(Speaker.photo == None).all():
    user = User2.query.filter(User2.email == speaker.email).first()
    if not user or not user.picture_url:
      continue
    print "Adding external picture for {}".format(speaker.email)
    response = requests.get(user.picture_url)
    speaker.photo = response.content

  db.session.commit()

  for speaker in Speaker.query.filter(Speaker.photo == None).all():
    email = speaker.email.lower()
    if 'oxiane' in email:
      continue

    size = 200
    hash = hashlib.md5(email.lower()).hexdigest()
    json_url = "http://www.gravatar.com/%s.json" % hash
    response = requests.get(json_url)
    if response.json() == u'User not found':
      continue

    print "Adding gravatar picture for {}".format(speaker.email)
    image_url = "http://www.gravatar.com/avatar/{}.jpg?s={}".format(hash, size)
    response = requests.get(image_url)
    speaker.photo = response.content

  db.session.commit()

  os.unlink(fn)
  return "OK"
