"""Excel importer
"""
from datetime import datetime
import traceback

import aniso8601
import xlrd
from website.crm.models import db, Room, Speaker, Track2, Talk


def parse_date(isodatestr):
  isodatestr = isodatestr.strip()
  if not isodatestr:
    return None
  return aniso8601.parse_datetime(isodatestr)


class Loader(object):
  def __init__(self, filename):
    self.wb = xlrd.open_workbook(filename)
    self._log = []
    self.rooms = {}
    self.speakers = {}
    self.tracks = {}

  def debug(self, msg):
    self._log.append(str(msg))

  @property
  def log(self):
    return "\n".join(self._log)

  def load(self):
    self.clean()
    self.load_rooms()
    self.load_speakers()
    self.load_tracks()
    self.load_talks()

  def clean(self):
    for cls in [Talk, Track2, Room, Speaker]:
      objs = cls.query.all()
      for obj in objs:
        db.session.delete(obj)
    db.session.flush()

  def load_rooms(self):
    self.debug("Parsing rooms")
    sheet = self.wb.sheet_by_name("Room")
    for i in range(1, sheet.nrows):
      self.debug("... {}".format(i))
      row = sheet.row(i)
      args = {
        'name': row[0].value,
        'capacity': row[1].value,
        'floor': row[2].value,
      }
      room = Room(**args)
      db.session.add(room)
      self.rooms[room.name] = room
    db.session.flush()

  def load_speakers(self):
    self.debug("Parsing speakers")
    sheet = self.wb.sheet_by_name("Speakers")
    for i in range(1, sheet.nrows):
      self.debug("... {}".format(i))
      row = sheet.row(i)

      keys = [
        'salutation',
        'first_name',
        'last_name',
        'organisation',
        'title',
        'email',
        'telephone',
        'bio_fr',
        'bio_en',
        'website',
        'twitter_handle',
        'github_handle',
        'sourceforge_handle',
        'linkedin_handle',
      ]
      args = {}
      for i, key in enumerate(keys):
        args[key] = row[i].value.strip()

      if not args['last_name']:
        self.debug("!! Speaker has no last name.")
        continue
      if args['website'] and not args['website'].startswith("http"):
        args['website'] = 'http://' + args['website']

      speaker = Speaker(**args)
      db.session.add(speaker)
      self.speakers[speaker.email] = speaker
    db.session.flush()

  def load_tracks(self):
    self.debug("Parsing tracks")
    sheet = self.wb.sheet_by_name("Tracks")
    for i in range(1, sheet.nrows):
      self.debug("... {}".format(i))
      row = sheet.row(i)
      try:
        self.load_track(row)
      except:
        self.debug(traceback.format_exc())

    db.session.flush()

  def load_track(self, row):
    room_name = row[0].value
    args = {
      'room': self.rooms.get(room_name),
      'name': row[1].value,
      'theme': row[2].value,
      'description_fr': row[3].value,
      'description_en': row[4].value,
      'starts_at': parse_date(row[5].value) or datetime(1970, 1, 1),
      'ends_at': parse_date(row[6].value) or datetime(1970, 1, 1),
    }
    track_leaders = []
    for i in range(7, 7 + 4):
      speaker_email = row[i].value
      if speaker_email:
        try:
          track_leaders.append(self.speakers[speaker_email])
        except KeyError:
          self.debug("Speaker: {} not fount".format(speaker_email))
    args['track_leaders'] = track_leaders
    track = Track2(**args)
    db.session.add(track)
    self.tracks[track.name] = track


  def load_talks(self):
    self.debug("Parsing talks")
    sheet = self.wb.sheet_by_name("Talk")
    for i in range(1, sheet.nrows):
      self.debug("... {}".format(i))
      row = sheet.row(i)
      try:
        self.load_talk(row)
      except:
        self.debug(traceback.format_exc())

    db.session.flush()

  def load_talk(self, row):
    args = {
      'type': row[0].value,
      'track': self.tracks[row[1].value],
      'title': row[2].value,
      'abstract_fr': row[3].value,
      'abstract_en': row[4].value,
      'starts_at': parse_date(row[5].value) or datetime(1970, 1, 1),
      'duration': int(row[6].value or 0),
      # 'lang': int(row[7].value),
    }

    speakers = []
    for i in range(8, 8 + 4):
      speaker_email = row[i].value
      if speaker_email:
        try:
          speakers.append(self.speakers[speaker_email])
        except KeyError:
          self.debug("Speaker: {} not fount".format(speaker_email))

    args['speakers'] = speakers

    talk = Talk(**args)
    db.session.add(talk)
