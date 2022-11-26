import os
import pymysql
from datetime import datetime
import json

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
                                   host='192.168.146.152', db='project_db'
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
        result = cursor.execute(
            'UPDATE tempo_users SET status = ' + str(status) + ' WHERE telegramId=' + user_tid + ';')
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


def get_role(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT role FROM users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                role = row[0]
            else:
                role = row['role']
        else:
            role = 0
    conn.close()
    return role


def get_status(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT status FROM users WHERE telegramId = ' + user_tid + ';')
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


def get_st_courses(user_tid):
    conn = open_connection()
    course_names = []
    course_ids = []
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT c.name, c.id FROM users AS a JOIN course_enrollments as b ON a.id = b.User_id JOIN courses AS c ON c.id = b.course_id WHERE a.telegramId=' + user_tid + ';')
        if result > 0:
            rows = cursor.fetchall()
            for row in rows:
                if type(row) is tuple:
                    course_names.append([row[0]])
                    course_ids.append([row[1]])
                else:
                    course_names.append([row['name']])
                    course_ids.append([row['id']])
        else:
            course_names = []
            course_ids = []
    conn.close()
    return [course_names, course_ids]


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


def update_dateauth(user_tid):
    conn = open_connection()
    now = datetime.now()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE users SET date_auth = "' + now.strftime("%Y:%m:%d %H:%M:%S") + '" WHERE telegramId=' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result


def update_datelast(user_tid):
    conn = open_connection()
    now = datetime.now()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE users SET last_interaction = "' + now.strftime("%Y:%m:%d %H:%M:%S") + '" WHERE telegramId=' + user_tid + ';')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_tid(user_tid, tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE users SET telegramId = ' + str(user_tid) + ' WHERE email= "' + tid + '";')
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def update_val1(user_tid, val1):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("UPDATE users SET val1 = '" + str(json.dumps(val1)) + "' WHERE telegramId= " + str(user_tid) + ";")
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result


def get_val1(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT val1 FROM users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                val1 = row[0]
            else:
                val1 = row['val1']
        else:
            val1 = "[[]]"
    conn.close()
    return json.loads(val1)


def get_st_classworks(user_course):
    conn = open_connection()
    classwork_names = []
    classwork_ids = []
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT b.name, b.id FROM courses AS a JOIN classworks as b ON a.id = b.course_id WHERE a.name = "' + user_course + '";')
        if result > 0:
            rows = cursor.fetchall()
            for row in rows:
                if type(row) is tuple:
                    classwork_names.append([row[0]])
                    classwork_ids.append([row[1]])
                else:
                    classwork_names.append([row['name']])
                    classwork_ids.append([row['id']])
        else:
            classwork_names = []
            classwork_ids = []
    conn.close()
    return [classwork_names, classwork_ids]

def get_val2(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT val2 FROM users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                val2 = row[0]
            else:
                val2 = row['val2']
        else:
            val2 = "[[]]"
    conn.close()
    return json.loads(val2)

def update_val2(user_tid, val2):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("UPDATE users SET val2 = '" + str(json.dumps(val2)) + "' WHERE telegramId= " + str(user_tid) + ";")
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result


def get_st_grade(user_tid, classword_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        print(classword_id)
        result = cursor.execute('SELECT a.grade FROM grades AS a JOIN users AS b ON b.id = a.user_id WHERE b.telegramId = ' + user_tid + ' AND a.classwork_id = ' + str(classword_id) + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                grade = row[0]
            else:
                grade = row['grade']
        else:
            grade = 0
    conn.close()
    return grade


def get_pr_courses(user_tid):
    conn = open_connection()
    course_names = []
    course_ids = []
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT b.name, b.id FROM users AS a JOIN courses AS b ON a.id = b.user_id WHERE a.telegramId=' + user_tid + ';')
        if result > 0:
            rows = cursor.fetchall()
            for row in rows:
                if type(row) is tuple:
                    course_names.append([row[0]])
                    course_ids.append([row[1]])
                else:
                    course_names.append([row['name']])
                    course_ids.append([row['id']])
        else:
            course_names = []
            course_ids = []
    conn.close()
    return [course_names, course_ids]

def get_pr_classworks(user_course):
    conn = open_connection()
    classwork_names = []
    classwork_ids = []
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT b.name, b.id FROM courses AS a JOIN classworks as b ON a.id = b.course_id WHERE a.name = "' + user_course + '";')
        if result > 0:
            rows = cursor.fetchall()
            for row in rows:
                if type(row) is tuple:
                    classwork_names.append([row[0]])
                    classwork_ids.append([row[1]])
                else:
                    classwork_names.append([row['name']])
                    classwork_ids.append([row['id']])
        else:
            classwork_names = []
            classwork_ids = []
    conn.close()
    return [classwork_names, classwork_ids]


def get_pr_students(user_tid, classwork_id):
    conn = open_connection()
    students_names = []
    students_gradeids = []
    students_classworkids = []
    with conn.cursor() as cursor:
        result = cursor.execute(
            'SELECT a.name, COALESCE(b.id, -1) AS id, COALESCE(b.grade, "*") AS grade '
            'FROM (SELECT b.name, b.id FROM course_enrollments AS a JOIN users AS b '
            'ON b.id = a.user_id WHERE a.course_id = (SELECT course_id '
            'FROM classworks WHERE id = ' + str(classwork_id) + ')) AS a LEFT JOIN (SELECT id, user_id, grade '
            'FROM grades WHERE classwork_id = ' + str(classwork_id) + ') AS b ON a.id = b.user_id;')
        if result > 0:
            rows = cursor.fetchall()
            for row in rows:
                if type(row) is tuple:
                    students_names.append([row[0] + " - " + row[2]])
                    students_gradeids.append([row[1]])
                else:
                    students_names.append([row['name'] + " - " + row['grade']])
                    students_gradeids.append([row['id']])
        else:
            students_names = []
            students_gradeids = []
    students_classworkids.append([classwork_id])
    conn.close()
    return [students_names, students_gradeids, students_classworkids]


def update_val3(user_tid, val3):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("UPDATE users SET val3 = '" + str(json.dumps(val3)) + "' WHERE telegramId= " + str(user_tid) + ";")
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result


def get_val3(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT val3 FROM users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                val3 = row[0]
            else:
                val3 = row['val3']
        else:
            val3 = "[[]]"
    conn.close()
    return json.loads(val3)

def update_val4(user_tid, val4):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("UPDATE users SET val4 = '" + str(json.dumps(val4)) + "' WHERE telegramId= " + str(user_tid) + ";")
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result


def get_val4(user_tid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT val4 FROM users WHERE telegramId = ' + user_tid + ';')
        if result > 0:
            row = cursor.fetchone()
            if type(row) is tuple:
                val4 = row[0]
            else:
                val4 = row['val4']
        else:
            val4 = "[[]]"
    conn.close()
    return json.loads(val4)


def upgrade_grade(grade_id, new_grade):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute(
            "UPDATE grades SET grade = '" + new_grade + "' WHERE id = " + grade_id + ";")
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result

def insert_grade(user_name, classwork_id, new_grade):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute(
            "INSERT INTO grades (classwork_id, grade, user_id) VALUES (" + classwork_id + ", " + new_grade +
            ", (SELECT id FROM users WHERE name = '" + user_name + "'));")
        if result > 0:
            conn.commit()
            print(cursor.lastrowid)
        else:
            pass
    conn.close()
    return result