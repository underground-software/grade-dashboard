#!/bin/env python

import datetime
from sql import grades_db_exec, \
	STUDENT_LATEST_SUBMISSION_REQ, ASSIGNMENT_LIST_REQ, \
	FIND_STUDENT_ID_REQ, INSERT_NEW_STUDENT_REQ

from orbit import ROOT, messageblock, appver, \
	get_authorized_user, AUTH_SERVER


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
	tuple_list = grades_db_exec(STUDENT_LATEST_SUBMISSION_REQ.format(student_id, assignment_id))
	if tuple_list:
		return Submission(tuple_list[0])
	return None

def build_page(student_id):
	page = "<h1>Student Dashboard</h1><br>"

	page += "<code>\n"
	page += str(get_assignment_list()[0])
	page += "</code>\n"

	return page

	# for assignment in get_assignment_list():
	#	page += build_assignment_table(get_latest_submission(student_id, assignment[0]), assignment[1])
	#	page += "<br>"
	# return page

def application(env, start_response):
	with open(ROOT + '/data/header') as header:
		page = header.read();
	username = get_authorized_user(AUTH_SERVER, env).lower()

	dbquery_result = grades_db_exec(FIND_STUDENT_ID_REQ.format(username))
	print(f'{dbquery_result}')

	# if not tuple_list:
	#	print('had to add student to db')
		# # need student ID!

	#	grades_db_exec(INSERT_NEW_STUDENT_REQ.format(student_id, username), commit=True)

	dbquery_result = grades_db_exec(FIND_STUDENT_ID_REQ.format(username))
	print(f'{dbquery_result}')
	page += build_page(dbquery_result)
	page += messageblock([('appver', appver())])
	start_response('200 OK', [('Content-Type', 'text/html')])
	return bytes(page, 'UTF-8')
