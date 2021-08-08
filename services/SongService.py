import typing
import mysql.connector as mariadb
from dotenv import load_dotenv
import os

load_dotenv()

if typing.TYPE_CHECKING:
    from dataTypes.Song import Song


class SongService:
    tableName = os.getenv("DB_TABLE_NAME")
    mariadb_connection = mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"))
    cursor = mariadb_connection.cursor()

    def save(self, song: 'Song'):
        self.cursor.execute(
            "INSERT INTO {} (name, artist, ranking, country, date)"
            " VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")"
            " ON DUPLICATE KEY UPDATE"
            " name=VALUES(name), "
            " artist=VALUES(artist), "
            " ranking=VALUES(ranking), "
            " country=VALUES(country), "
            " date=VALUES(date)".format(
                self.tableName,
                song.name,
                song.author,
                song.ranking,
                song.country,
                song.date
            )

        )
        self.mariadb_connection.commit()
