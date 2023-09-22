#!/bin/env python
import sys, os, sqlite3


INSERT_SUB="""
INSERT INTO submissions (sub_id, user, time)
VALUES ("{}","{}","{}");
""".strip()

GET_SUB_BY_ID="""
SELECT sub_id, user, time
FROM submissions
WHERE sub_id = "{}";
""".strip()

GET_SUB_BY_USER="""
SELECT sub_id, user, time
FROM submissions
WHERE user = "{}";
""".strip()

TA_DIR=os.path.dirname(os.path.abspath(__file__))
GRADES_DB=f'{TA_DIR}/grades.db'

def add_sub(sub_id, user, time):
    do_sqlite3_comm(GRADES_DB, INSERT_SUB.format(sub_id, user, time), commit=True)

def get_sub_by_id(sub_id):
    return do_sqlite3_comm(GRADES_DB, GET_SUB_BY_ID.format(sub_id), fetch=True)

def get_sub_by_user(sub_id):
    return do_sqlite3_comm(GRADES_DB, GET_SUB_BY_USER.format(sub_id), fetch=True)

DP=lambda x: print(x, file=sys.stderr)

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
