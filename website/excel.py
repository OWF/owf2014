"""Excel importer
"""

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
    self.log = []
    self.rooms = {}
    self.speakers = {}
    self.tracks = {}

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
    self.log.append("Parsing rooms")
    sheet = self.wb.sheet_by_name("Room")
    for i in range(1, sheet.nrows):
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
    self.log.append("Parsing speakers")
    sheet = self.wb.sheet_by_name("Speakers")
    for i in range(1, sheet.nrows):
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
      speaker = Speaker(**args)
      db.session.add(speaker)
      self.speakers[speaker.email] = speaker
    db.session.flush()

  def load_tracks(self):
    self.log.append("Parsing tracks")
    sheet = self.wb.sheet_by_name("Tracks")
    for i in range(1, sheet.nrows):
      row = sheet.row(i)
      room_name = row[0].value
      args = {
        'room': self.rooms.get(room_name),
        'name': row[1].value,
        'theme': row[2].value,
        'description_fr': row[3].value,
        'description_en': row[4].value,
        'starts_at': parse_date(row[5].value),
        'ends_at': parse_date(row[6].value),
      }
      track_leaders = []
      for i in range(7, 7 + 4):
        speaker_email = row[i].value
        if speaker_email:
          track_leaders.append(self.speakers[speaker_email])
      args['track_leaders'] = track_leaders
      track = Track2(**args)
      db.session.add(track)
      self.tracks[track.name] = track

    db.session.flush()

  def load_talks(self):
    self.log.append("Parsing talks")
    sheet = self.wb.sheet_by_name("Talk")
    for i in range(1, sheet.nrows):
      row = sheet.row(i)
      args = {
        'type': row[0].value,
        'track': self.tracks[row[1].value],
        'title': row[2].value,
        'abstract_fr': row[3].value,
        'abstract_en': row[4].value,
        'starts_at': parse_date(row[5].value),
        'duration': int(row[6].value or 0),
        #'lang': int(row[7].value),
      }

      speakers = []
      for i in range(8, 8 + 4):
        speaker_email = row[i].value
        if speaker_email:
          speakers.append(self.speakers[speaker_email])
      args['speakers'] = speakers

      talk = Talk(**args)
      db.session.add(talk)

    db.session.flush()
