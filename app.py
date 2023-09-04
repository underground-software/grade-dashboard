from config import *
import sqlite3
import datetime

# CURRENTLY HARD CODING THE STUDENT WHOSE DASHBOARD IS SHOWN
CURR_STUDENT_ID = 2







STUDENT_LATEST_SUBMISSION_REQ = """\
SELECT
	s.submission_id,
	s.student_id,
	s.assignment_id,
	s.submission_name,
	MAX(s.submission_date) as submission_date,
	s.submission_grade,
	s.submission_comments
FROM
	submissions s
WHERE
	student_id = %s
AND
	assignment_id = %s
;
"""

ASSIGNMENT_LIST_REQ = """\
SELECT
	*
FROM
	assignments
;
"""

ASSIGNMENT_TABLE_TEMPLATE = """
<table>
	<caption> %s </caption>
	<tr>
		<th> Grade </th>
		<th> Comments </th>
		<th> Time Recieved </th>
	</tr>
	<tr>
		<th> %s </th>
		<th> %s </th>
		<th> %s </th>
	</tr>
</table>
"""

class Submission:
	def __init__(self, submission_tuple):
		self.submission_id = submission_tuple[0]
		self.student_id = submission_tuple[1]
		self.assignment_id = submission_tuple[2]
		self.name = submission_tuple[3]
		self.date = submission_tuple[4]
		self.grade = submission_tuple[5]
		self.comments = submission_tuple[6]

	def __repr__(self):
		return "%s %s %s %s %s %s %s" % \
			(self.submission_id, self.student_id, self.assignment_id, self.name, self.date, self.grade, self.comments)

def or_dash(s):
	return s if s else "-"

def build_assignment_table(sub, assignment_name):
	dt = "-"
	if sub and sub.date:
		dt = datetime.datetime.fromtimestamp(sub.date).strftime("%Y-%m-%d %H:%M:%S")
	

	return ASSIGNMENT_TABLE_TEMPLATE % (assignment_name, or_dash(sub.grade), or_dash(sub.comments), dt)

def grades_db_exec(command):
	result = None
	con = sqlite3.connect(GRADES_DB)
	cur = con.cursor()
	cur2 = cur.execute(command)
	res = cur2.fetchall()

	con.close()
	return res

def get_assignment_list():
	return grades_db_exec(ASSIGNMENT_LIST_REQ)

def get_latest_submission(student_id, assignment_id):
	tuple_list = grades_db_exec(STUDENT_LATEST_SUBMISSION_REQ % (student_id, assignment_id))
	if tuple_list:
		return Submission(tuple_list[0])
	return None

def build_page(student_id):
	page = ""
	for assignment in get_assignment_list():
		page += build_assignment_table(get_latest_submission(student_id, assignment[0]), assignment[1])
		page += "<br>"
	return page

def application(env, start_response):
	page = """
	<head>
		<style>
			table, th, td {
				border: 1px solid;
			}
		</style>
	</head>
	"""
	page += build_page(CURR_STUDENT_ID)
	start_response('202 OK', [('Content-Type', 'text/html')])
	return bytes(page, 'UTF-8')
