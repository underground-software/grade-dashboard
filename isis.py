#!/bin/env python

# builds the 'international student information system' html table

from datetime import datetime
import random
from common import get_sub_by_user, get_ass

from orbit import table

def isis_table(ass_pair, subs):
    fmt = []
    fmt += [('Submission #', 'Time Recieved', 'Summary',  'Comment', 'Grade')]

    i = 0
    for sub in subs:
        fmt += [(i, str(datetime.fromtimestamp(sub[2])), 'lorem', 'ipsum',
            random.choices(['A','B','C','D','F'])[0])]
        i += 1

    return table(fmt)

# REVISION INDEX | DATETIME RECV | COMMENTS | GRADE
def isis(user):
    subs = get_sub_by_user(user)

    fmt = []
    fmt += [('Submission #', 'Time Recieved', 'Summary',  'Comment', 'Grade')]
    ass = get_ass()

    output =''
    output += f"<h1> {user}'s dashboard</h1>"

    for ass_pair in ass:
        output += f'<h3>{ass_pair[0]}: {ass_pair[1]}</h3>'
        output += isis_table(fmt, subs)

    return output

def main():
    print(isis("joel"))

if __name__ == "__main__":
    main()
