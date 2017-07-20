from peewee import *
from urllib.parse import urlparse
import psycopg2, os

# for heroku db connection
url = urlparse(os.environ["DATABASE_URL"])
db  = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
     )

# model definition
class Player(Model):
    lineId      = CharField()
    displayName = CharField()

    class Meta:
        database = db

    def __init__(self, lineId, displayName):
        super(Player, self).__init__()
        self.lineId = lineId
        self.displayName = displayName
