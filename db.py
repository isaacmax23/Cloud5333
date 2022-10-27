# db.py
import os
import pymysql
from flask import jsonify

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_connection_name = os.environ.get('INSTANCE_UNIX_SOCKET')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        # if os.environ.get('GAE_ENV') == 'standard':
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name,
                               cursorclass=pymysql.cursors.DictCursor
                               )
    except pymysql.MySQLError as e:
        print("here", e)

    return conn


def get_songs():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM userEmail;')
        songs = cursor.fetchall()
        if result > 0:
            got_songs = jsonify(songs)
        else:
            got_songs = 'No Songs in DB'
    conn.close()
    return got_songs

# def add_songs(song):
#     conn = open_connection()
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO userEmail (id, artist, genre) VALUES(%s, %s, %s)', (song["title"], song["artist"], song["genre"]))
#     conn.commit()
#     conn.close()
