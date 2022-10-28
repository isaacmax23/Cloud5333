import os
import pymysql

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_connection_name = os.environ.get('INSTANCE_UNIX_SOCKET')

def open_connection():
    local = False

    unix_socket = '/cloudsql/{}'.format(db_connection_name)

    try:
        if not local:
            if os.environ.get('GAE_ENV') == 'standard':
                conn = pymysql.connect(user=db_user, password=db_password,
                                       unix_socket=unix_socket, db=db_name,
                                       cursorclass=pymysql.cursors.DictCursor
                                   )
        else:
            conn = pymysql.connect(user='test', password='test',
                                   host='192.168.0.108', db='project_db'
                                   )
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
            row = cursor.fetchone()
            if type(row) is tuple:
                code = row[0]
            else:
                code = row['code']
        else:
            code = 0
    conn.close()
    return code

def get_tempoemail(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT email FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                email = row[0]
            else:
                email = row['email']
        else:
            email = 0
    conn.close()
    return email

def get_tempostatus(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT status FROM tempo_users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                status = row[0]
            else:
                status = row['status']
        else:
            status = 0
    conn.close()
    return status

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
