#!/bin/env python

import datetime
from sql import grades_db_exec, \
    STUDENT_LATEST_SUBMISSION_REQ, ASSIGNMENT_LIST_REQ, \
    FIND_STUDENT_ID_REQ, INSERT_NEW_STUDENT_REQ

from loguru import logger

from orbit import ROOT, messageblock, appver, \
    get_authorized_user, AUTH_SERVER, table

from isis import isis_table

def ta_log(msg):
    logger.info(f'ATA: {msg}')

def build_assignments_list():
    res = []
    with open('assignments.list' ,'r') as f:
        for line in f:
            # comment
            if line[0] == '#':
                continue
            res += (line.split(' '))
    return res

def make_assignment_table(foobar):
   return table([('Grade', 'Comments', 'Time Recieved')])

def build_assignment_table(sub, assignment_name):
    dt = "-"
    if sub and sub.date:
        dt = datetime.datetime.fromtimestamp(sub.date).strftime("%Y-%m-%d %H:%M:%S")

    return ASSIGNMENT_TABLE_TEMPLATE % (assignment_name, or_dash(sub.grade), or_dash(sub.comments), dt)

def get_assignment_list():
    return grades_db_exec(ASSIGNMENT_LIST_REQ)

def get_latest_submission(sid, assignment_id):
    tuple_list = grades_db_exec(STUDENT_LATEST_SUBMISSION_REQ.format(sid, assignment_id))
    if tuple_list:
        return Submission(tuple_list[0])
    return None

def old_build_page(sid):
    for assignment in build_assignments_list():
        print(assignment)

    page = "<h1>Student Dashboard</h1><br>"

    page += "<code>\n"
    #page += str(get_assignment_list()[0])
    page = make_assignment_table(1)
    page += "</code>\n"

    return page

def autorefresh_text(interval):
    return bytes(f'<meta http-equiv="refresh" content="{interval}">', "UTF-8")

REFRESH_INTERVAL=2
def build_page(user, sid, path):
    if path == "/tab":
        return isis_table(user)
    return old_build_page(sid)

def get_id_by_user(user):
    # TODO
    return 45

def gather_id(env):
    path = env.get('PATH_INFO', '/dashboard')
    ta_log(f'path: {path}')

    user = get_authorized_user(AUTH_SERVER, env)
    ta_log(f'new login by: {user}')

    # TODO
    sid = get_id_by_user(user)

    ta_log(f'found student id: {sid}')

    return (user, sid, path)

def application(env, SR):
    path = env.get('PATH_INFO', '/dashboard')
    ta_log(f'path: {path}')

    if path == "/devheader":
        SR('200 OK', [('Content-Type', 'text/plain')])
        return autorefresh_text(REFRESH_INTERVAL)

    (user, sid, path) = gather_id(env)
    page = ""

    with open(ROOT + '/data/header') as header:
        page += header.read();

    page += build_page(user, sid, path)
    page += messageblock([('appver', appver())])

    SR('200 OK', [('Content-Type', 'text/html')])

    return bytes(page, 'UTF-8')
