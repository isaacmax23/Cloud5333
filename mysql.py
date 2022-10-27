import os
import pymysql

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_connection_name = os.environ.get('INSTANCE_UNIX_SOCKET')

# db_user = 'test'
# db_password = 'test'
# db_name = 'project_db'
# db_connection_name = '192.168.0.107'


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)

    try:
        if os.environ.get('GAE_ENV') == 'standard':
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name,
                               cursorclass=pymysql.cursors.DictCursor
                               )
        # conn = pymysql.connect(user=db_user, password=db_password,
        #                        host=db_connection_name, db=db_name
        #                        )
    except pymysql.MySQLError as e:
        print("Error: ", e)

    return conn


def check_email(user_email):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM users WHERE email = "' + user_email + '";')
        if result > 0:
            is_email = True
        else:
            is_email = False
    conn.close()
    return is_email


def check_tid(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            is_tid = True
        else:
            is_tid = False
    conn.close()
    return is_tid

def check_tempotid(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            is_tempotid = True
        else:
            is_tempotid = False
    conn.close()
    return is_tempotid

def get_tempostatus(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT status FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            status = cursor.fetchone()[0]
        else:
            status = 0
    conn.close()
    return status

def insert_tempouser(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('INSERT INTO tempo_users (telegramId, status, code) VALUES (' + user_tid + ',1,1);')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_tempostatus(user_tid, status):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE tempo_users SET status = ' + str(status) + ' WHERE telegramId=' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_tempocode(user_tid, code):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE tempo_users SET code = ' + str(code) + ' WHERE telegramId=' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_tempoemail(user_tid, email):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE tempo_users SET email = "' + email + '" WHERE telegramId=' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def get_tempocode(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT code FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            code = cursor.fetchone()[0]
        else:
            code = 0
    conn.close()
    return code

def get_tempoemail(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT email FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            code = cursor.fetchone()[0]
        else:
            code = 0
    conn.close()
    return code

def delete_tempouser(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('DELETE FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_status(user_tid, status):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE users SET status = ' + str(status) + ' WHERE telegramId=' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_tid(user_tid, email):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE users SET telegramId = ' + str(user_tid) + ' WHERE email= "' + email + '";')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result
