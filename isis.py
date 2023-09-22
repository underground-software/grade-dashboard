#!/bin/env python

# builds the 'international student information system' html table

from datetime import datetime
import random
from common import get_sub_by_user

from orbit import table

# REVISION INDEX | DATETIME RECV | COMMENTS | GRADE
def isis_table(user):
    subs = get_sub_by_user(user)

    fmt = []
    fmt += [('Submission #', 'Time Recieved', 'Summary',  'Comment', 'Grade')]

    i = 0
    for sub in subs:
        fmt += [(i, str(datetime.fromtimestamp(sub[2])), 'lorem', 'ipsum', random.choices(['A','C','F'])[0])]
        i += 1

    output = table(fmt)

    return output

def main():
    print(isis_table("joel"))

if __name__ == "__main__":
    main()
