from sqlalchemy import Table, MetaData, create_engine, select
import csv

meta = MetaData()
engine = create_engine('sqlite:///abilian.db')
connection = engine.connect()

speaker_table = Table('speaker', meta, autoload=True, autoload_with=engine)

s = select([speaker_table])
output_file = open("speakers.csv", "wc")
writer = csv.writer(output_file)


for speaker in connection.execute(s).fetchall():
  t = [
    speaker.salutation,
    speaker.first_name,
    speaker.last_name,
    speaker.organisation,
    speaker.title,
    speaker.email,
    speaker.telephone,
    "",
    speaker.bio,
    speaker.website,
    speaker.twitter_handle,
    speaker.github_handle,
    speaker.sourceforge_handle,
    "",
  ]
  print t
  t = [x.encode("utf8") if isinstance(x, basestring) else "" for x in t]
  writer.writerow(t)

  if speaker.photo:
    open("photos/{}.jpg".format(speaker.email), "wc").write(speaker.photo)
