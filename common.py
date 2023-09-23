#!/bin/env python
import sys, os, sqlite3


INSERT_SUB="""
INSERT INTO submissions (sub_id, user, time, _from, _to, email_ids, subjects)
VALUES ("{}","{}","{}","{}","{}","{}","{}");
""".strip()

GET_SUB_BY_ID="""
SELECT sub_id, user, time, _from, _to, email_ids, subjects
FROM submissions
WHERE sub_id = "{}";
""".strip()

GET_SUB_BY_USER="""
SELECT sub_id, user, time, _from, _to, email_ids, subjects
FROM submissions
WHERE user = "{}";
""".strip()

GET_ASS_BY_EMAIL_ID="""
SELECT web_id, email_id
FROM assignments
WHERE email_id = "{}";
""".strip()

GET_ASS_BY_WEB_ID="""
SELECT web_id, email_id
FROM assignments
WHERE web_id = "{}";
""".strip()

GET_ASS="""
SELECT *
FROM assignments;
""".strip()

TA_DIR=os.path.dirname(os.path.abspath(__file__))
GRADES_DB=f'{TA_DIR}/grades.db'

def add_sub(sub_id, user, timestamp, frs, tos, email_ids, sbj):
    cmd=INSERT_SUB.format(sub_id, user, timestamp, \
            frs[0], tos[0], ",".join(email_ids), ",".join(sbj))
    print("running sql:", cmd, "end\nend")
    do_sqlite3_comm(GRADES_DB, cmd, commit=True)

def get_sub_by_id(sub_id):
    return do_sqlite3_comm(GRADES_DB, GET_SUB_BY_ID.format(sub_id), fetch=True)

def get_sub_by_user(sub_id):
    return do_sqlite3_comm(GRADES_DB, GET_SUB_BY_USER.format(sub_id), fetch=True)

def get_ass_by_web_id(web_id):
    return do_sqlite3_comm(GRADES_DB, GET_ASS_BY_WEB_ID.format(web_id), fetch=True)

def get_ass():
    return do_sqlite3_comm(GRADES_DB, GET_ASS, fetch=True)

def get_ass_by_email_id(email_id):
    return do_sqlite3_comm(GRADES_DB, GET_ASS_BY_WEB_ID.format(email_id), fetch=True)

DP=lambda x: print(x, file=sys.stdout)

def do_sqlite3_comm(db, comm, commit=False, fetch=False):
    result=None
    DP(f'CONNECT TO {db}')
    db_con = sqlite3.connect(db)
    db_cur0 = db_con.cursor()
    DP("RUN SQL: %s" % comm)
    db_cur1 = db_cur0.execute(comm)

    if fetch:
        result=db_cur1.fetchall()
        DP("SQL RES: %s" % str(result))

    if commit:
        DP("RUN SQL: COMMIT;")
        db_cur2 = db_cur1.execute("COMMIT;")

    db_con.close()

    return result
