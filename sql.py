#!/usr/bin/env python

import sqlite3

DB_FILENAME='grades.db'

def do_sqlite3_comm(db, comm, commit=False, fetch=False):
	result=None
	db_con = sqlite3.connect(db)
	db_cur0 = db_con.cursor()
	
	db_cur1 = db_cur0.execute(comm)

	if fetch:
		result=db_cur1.fetchone()

	if commit:
		db_cur2 = db_cur1.execute("COMMIT;")

	db_con.close()

	return result

STUDENT_LATEST_SUBMISSION_REQ="""
SELECT (submission_id, student_id, assignment_id,
    submission_name, submission_grade, submission_comments)
FROM submissions
WHERE student_id = '{}'
AND assignment_id = '{}';
""".strip()


ASSIGNMENT_LIST_REQ="""
SELECT *
FROM assignments;
""".strip()

FIND_STUDENT_ID_REQ="""
SELECT student_id
FROM students
WHERE username = '{}';
""".strip()

INSERT_NEW_STUDENT_REQ="""
INSERT INTO students (student_id, username)
VALUES ('{}', '{}');
""".strip()

def grades_db_exec(cmd, commit=False):
    print(f"RUN SQL '{cmd}'")
    result = do_sqlite3_comm(DB_FILENAME, cmd, fetch=True, commit=commit)

    return result
