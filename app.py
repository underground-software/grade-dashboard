from sql import grades_db_exec, STUDENT_LATEST_SUBMISSION_REQ, ASSIGNMENT_LIST_REQ, FIND_STUDENT_ID_REQ, INSERT_NEW_STUDENT_REQ
import datetime
from orbit import ROOT, messageblock, appver, get_authorized_user


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

def get_assignment_list():
	return grades_db_exec(ASSIGNMENT_LIST_REQ)

def get_latest_submission(student_id, assignment_id):
	tuple_list = grades_db_exec(STUDENT_LATEST_SUBMISSION_REQ % (student_id, assignment_id))
	if tuple_list:
		return Submission(tuple_list[0])
	return None

def build_page(student_id):
	page = "<h1>Student Dashboard</h1><br>"
	for assignment in get_assignment_list():
		page += build_assignment_table(get_latest_submission(student_id, assignment[0]), assignment[1])
		page += "<br>"
	return page

def application(env, start_response):
	with open(ROOT + '/data/header') as header:
		page = header.read();
	username = get_authorized_user('', env).lower()
	tuple_list = grades_db_exec(FIND_STUDENT_ID_REQ % username)
	print(f'{tuple_list=}')
	if not tuple_list:
		print('had to add student to db')
		grades_db_exec(INSERT_NEW_STUDENT_REQ % username, commit=True)
	tuple_list = grades_db_exec(FIND_STUDENT_ID_REQ % username)
	((CURR_STUDENT_ID),), = tuple_list
	print(f'{CURR_STUDENT_ID=}')
	page += build_page(CURR_STUDENT_ID)
	page += messageblock([('appver', appver())])
	start_response('200 OK', [('Content-Type', 'text/html')])
	return bytes(page, 'UTF-8')
