from flask import Flask, render_template, request, g
from mysql import check_email, check_tid, check_tempotid, insert_tempouser, get_tempostatus, update_tempostatus, \
    update_tempocode, get_tempocode, delete_tempouser, update_tempoemail, update_status, update_tid, get_tempoemail, \
    get_role, get_status, update_dateauth, get_st_courses, update_datelast, update_val1, get_val1, get_st_classworks, \
    get_val2, update_val2, get_st_grade, get_pr_courses, get_pr_students, update_val3, get_val3, update_val4, \
    get_val4, upgrade_grade, insert_grade, get_session_time, update_maxauth, get_auth_time, get_max_auth, reset_tid

from telegram import send_message, send_message_with_reply
from google.cloud import pubsub_v1
import random
import json
app = Flask(__name__)

project_id = "top-cubist-365802"
topic_id = "otp-email-list"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def sendMail(email, code):
    x = {
        "receiver_email": email,
        "subject": "Authentication Code - Virtual TA",
        "message": str(code)
    }
    data_str = json.dumps(x)
    data = data_str.encode("utf-8")
    # When you publish a message, the client returns a future.
    future1 = publisher.publish(topic_path, data)
    print(future1.result())

def main_menu(user_id):
    if get_role(user_id):
        send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Get Grade"], ["Options"]])
        update_status(user_id, 2)
    else:
        send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Update Grade"], ["Options"]])
        update_status(user_id, 7)
@app.route('/', methods = ['POST'])



def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    user_id = request.form['id']
    user_message = request.form['message']
    code = 0
    if check_tid(user_id) and get_auth_time(user_id) > get_max_auth(user_id):
        print('Auth time: ' + str(get_auth_time(user_id)))
        reset_tid(user_id)
        update_status(user_id, 0)
    if check_tid(user_id):
        session_time = get_session_time(user_id)
        update_datelast(user_id)
        status = get_status(user_id)
        if status == 1 or session_time > 30:
            main_menu(user_id)
        elif status == 2:
            if user_message == 'Get Grade':
                courses = get_st_courses(user_id)
                update_val1(user_id, courses)
                courses[0].append(['Back to Main Menu'])
                update_status(user_id, 3)
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses[0])
            elif user_message == 'Options':
                update_status(user_id, 13)
                send_message_with_reply(user_id, "__VTA__ \-\> Select option", [["Authorization Max Time"],["Back to Main Menu"]])
            else:
                send_message(user_id, "Please select one option from menu")
        elif status == 3:
            courses = get_val1(user_id)[0]
            if user_message == 'Back to Main Menu':
                send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Get Grade"], ["Options"]])
                update_status(user_id, 2)
            elif [user_message] in courses:
                classworks = get_st_classworks(user_message)
                update_val2(user_id, classworks)
                classworks[0].append(['Back to Courses'])
                classworks[0].append(['Back to Main Menu'])
                update_status(user_id, 4)
                send_message_with_reply(user_id, "__VTA__ \-\> Select classwork:", classworks[0])
            else:
                send_message(user_id, "Please select one option from menu")
        elif status == 4:
            classworks = get_val2(user_id)
            classwork_ids = classworks[1]
            classwork_names = classworks[0]
            if user_message == 'Back to Main Menu':
                send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Get Grade"], ["Options"]])
                update_status(user_id, 2)
            elif user_message == 'Back to Courses':
                courses = get_val1(user_id)[0]
                courses.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses)
                update_status(user_id, 3)
            elif [user_message] in classwork_names:
                classwork_id = classwork_ids[classwork_names.index([user_message])]
                grade = get_st_grade(user_id, classwork_id[0])
                grade_menu = []
                grade_menu.append(['Back to Classworks'])
                grade_menu.append(['Back to Courses'])
                grade_menu.append(['Back to Main Menu'])
                update_status(user_id, 5)
                send_message_with_reply(user_id, "__VTA__ \-\> Grade: " + str(grade), grade_menu)
            else:
                send_message(user_id, "Please select one option from menu")
        elif status == 5:
            if user_message == 'Back to Main Menu':
                send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Get Grade"], ["Options"]])
                update_status(user_id, 2)
            elif user_message == 'Back to Courses':
                courses = get_val1(user_id)[0]
                courses.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses)
                update_status(user_id, 3)
            elif user_message == 'Back to Classworks':
                classworks = get_val2(user_id)[0]
                classworks.append(['Back to Courses'])
                classworks.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select classwork:", classworks)
                update_status(user_id, 4)
        elif status == 7:
            if user_message == 'Update Grade':
                courses = get_pr_courses(user_id)
                update_val1(user_id, courses)
                courses[0].append(['Back to Main Menu'])
                update_status(user_id, 8)
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses[0])
            elif user_message == 'Options':
                update_status(user_id, 13)
                send_message_with_reply(user_id, "__VTA__ \-\> Select option",
                                        [["Authorization Max Time"], ["Back to Main Menu"]])
            else:
                send_message(user_id, "Please select one option from menu")
        elif status == 8:
                courses = get_val1(user_id)[0]
                if user_message == 'Back to Main Menu':
                    send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Update Grade"], ["Options"]])
                    update_status(user_id, 7)
                elif [user_message] in courses:
                    classworks = get_st_classworks(user_message)
                    update_val2(user_id, classworks)
                    classworks[0].append(['Back to Courses'])
                    classworks[0].append(['Back to Main Menu'])
                    update_status(user_id, 9)
                    send_message_with_reply(user_id, "__VTA__ \-\> Select classwork:", classworks[0])
                else:
                    send_message(user_id, "Please select one option from menu")
        elif status == 9:
            classworks = get_val2(user_id)
            classwork_ids = classworks[1]
            classwork_names = classworks[0]
            if user_message == 'Back to Main Menu':
                send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Update Grade"], ["Options"]])
                update_status(user_id, 7)
            elif user_message == 'Back to Courses':
                courses = get_val1(user_id)[0]
                courses.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses)
                update_status(user_id, 8)
            elif [user_message] in classwork_names:
                classwork_id = classwork_ids[classwork_names.index([user_message])]
                students = get_pr_students(user_id, classwork_id[0])
                update_val3(user_id, students)
                students[0].append(['Back to Classworks'])
                students[0].append(['Back to Courses'])
                students[0].append(['Back to Main Menu'])
                update_status(user_id, 10)
                send_message_with_reply(user_id, "__VTA__ \-\> Select student: ", students[0])
            else:
                send_message(user_id, "Please select one option from menu")
        elif status == 10:
            students = get_val3(user_id)
            students_gradeids = students[1]
            students_names = students[0]
            students_classworkid = students[2][0]
            if user_message == 'Back to Main Menu':
                send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Update Grade"], ["Options"]])
                update_status(user_id, 7)
            elif user_message == 'Back to Courses':
                courses = get_val1(user_id)[0]
                courses.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses)
                update_status(user_id, 8)
            elif user_message == 'Back to Classworks':
                classworks = get_val2(user_id)[0]
                classworks.append(['Back to Courses'])
                classworks.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select classwork:", classworks)
                update_status(user_id, 9)
            elif [user_message] in students_names:
                grade_id = students_gradeids[students_names.index([user_message])]
                student = user_message.split(' - ')[0]
                grade = user_message.split(' - ')[1]
                if grade == '*':
                    val4 = [students_classworkid, student]
                    update_status(user_id, 11)
                else:
                    val4 = [students_classworkid, grade_id]
                    update_status(user_id, 12)
                update_val4(user_id, val4)
                st_grade_menu = []
                st_grade_menu.append(['Back to Students'])
                st_grade_menu.append(['Back to Classworks'])
                st_grade_menu.append(['Back to Courses'])
                st_grade_menu.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Type the new grade: ", st_grade_menu)
            else:
                send_message(user_id, "Please select one option from menu")
        elif status == 11 or status == 12:
            new_grade_info = get_val4(user_id)
            grade_classwork_id = new_grade_info[0]
            new_grade_data = new_grade_info[1]
            if user_message == 'Back to Main Menu':
                send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Update Grade"], ["Options"]])
                update_status(user_id, 7)
            elif user_message == 'Back to Courses':
                courses = get_val1(user_id)[0]
                courses.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select course:", courses)
                update_status(user_id, 8)
            elif user_message == 'Back to Classworks':
                classworks = get_val2(user_id)[0]
                classworks.append(['Back to Courses'])
                classworks.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select classwork:", classworks)
                update_status(user_id, 9)
            elif user_message == 'Back to Students':
                students = get_val3(user_id)[0]
                students.append(['Back to Classworks'])
                students.append(['Back to Courses'])
                students.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select student:", students)
                update_status(user_id, 10)
            elif user_message.strip().isdigit() and int(user_message.strip()) < 101:
                new_grade = user_message.strip()
                if status == 11:
                    insert_grade(new_grade_data, str(grade_classwork_id[0]), new_grade)
                if status == 12:
                    upgrade_grade(str(new_grade_data[0]), new_grade)
                students = get_pr_students(user_id, grade_classwork_id[0])
                update_val3(user_id, students)
                students[0].append(['Back to Classworks'])
                students[0].append(['Back to Courses'])
                students[0].append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select student:", students[0])
                update_status(user_id, 10)
            else:
                send_message(user_id, "Please provide a correct grade")
        elif status == 13:
            if user_message == 'Back to Main Menu':
                main_menu(user_id)
            elif user_message == 'Authorization Max Time':
                options = []
                options.append(['5 min'])
                options.append(['1 hour'])
                options.append(['1 day'])
                options.append(['1 week'])
                options.append(['1 month'])
                options.append(['Back to Options'])
                options.append(['Back to Main Menu'])
                send_message_with_reply(user_id, "__VTA__ \-\> Select Max Auth Time", options)
                update_status(user_id, 14)
            else:
                send_message(user_id, "Please provide a correct grade")
        elif status == 14:
            if user_message == 'Back to Main Menu':
                if get_role(user_id):
                    send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Get Grade"], ["Options"]])
                    update_status(user_id, 2)
                else:
                    send_message_with_reply(user_id, "__VTA__ \-\> Main Menu", [["Update Grade"], ["Options"]])
                    update_status(user_id, 7)
            if user_message == 'Back to Options':
                update_status(user_id, 13)
                send_message_with_reply(user_id, "__VTA__ \-\> Select option",
                                        [["Authorization Max Time"], ["Back to Main Menu"]])
            elif user_message in ['5 min', '1 hour', '1 day', '1 week', '1 month']:
                new_time = 5
                if user_message == '5 min':
                    new_time = 5
                if user_message == '1 hour':
                    new_time = 60
                if user_message == '1 day':
                    new_time = 1440
                if user_message == '1 week':
                    new_time = 10080
                if user_message == '1 month':
                    new_time = 302400
                update_maxauth(user_id, new_time)
                update_status(user_id, 13)
                send_message_with_reply(user_id, "__VTA__ \-\> Select option",
                                        [["Authorization Max Time"], ["Back to Main Menu"]])
            else:
                send_message(user_id, "Please provide a correct grade")

    else:
        if check_tempotid(user_id):
            tempo_status = get_tempostatus(user_id)
            if tempo_status == 1:
                if check_email(user_message):
                    code = random.randint(1000,9999)
                    sendMail(user_message, code)
                    update_tempostatus(user_id, 2)
                    update_tempocode(user_id, code)
                    update_tempoemail(user_id, user_message)
                    send_message(user_id, '__LOGIN__ \-\> Provide the code sent to email')
                else:
                    send_message(user_id, '__LOGIN__ \-\> Email not found')
                    delete_tempouser(user_id)
            if tempo_status == 2:
                if str(get_tempocode(user_id)) == user_message:
                    update_tid(user_id, get_tempoemail(user_id))
                    update_status(user_id, 1)
                    update_dateauth(user_id)
                    delete_tempouser(user_id)
                    if get_role(user_id):
                        send_message(user_id, ' You are logged in as Student')
                    else:
                        send_message(user_id, ' You are logged in as Professor')
                    main_menu(user_id)
                    # send_message(user_id, '__LOGIN__ \-\> Write "hello" to begin')
                else:
                    send_message(user_id, '__LOGIN__ \-\> Code not correct')
                    delete_tempouser(user_id)
        else:
            print(insert_tempouser(user_id))
            send_message(user_id, '__LOGIN__ \-\> Provide your UTA email')
    print(user_message + "-" + str(code))
    return render_template('index.html', userm=user_message + "-" + str(code))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)