from peewee import *
from urllib.parse import urlparse
import psycopg2, os

# for heroku db connection

if 'HEROKU' in os.environ:
  url = urlparse(os.environ["DATABASE_URL"])
  db  = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
  )
else: 
  db = PostgresqlDatabase(
    database = 'janken',
    user     = 'yoshiharu-i',
    host     = 'localhost'
  )
 
# model definition
class PostgresqlModel(Model):
  """ A base model """
  class Meta:
    database = db

class Player(PostgresqlModel):
    lineId      = CharField()
    displayName = CharField()
    win         = IntegerField(default=0)
    lose        = IntegerField(default=0)
