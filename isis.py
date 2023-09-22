#!/bin/env python

# builds the 'international student information system' html table

from orbit import table

from common import get_sub_by_user

# REVISION INDEX | DATETIME RECV | COMMENTS | GRADE
def isis_table(user):

    subs = get_sub_by_user(user)
    print("SUBS")
    print(subs)
    i=0
    for sub in subs:
        print("SUB ", i)
        i+=1
        print(sub)
    

    fmt = []
    fmt += [('Submission #', 'Summary',  'Comment', 'Grade')]
    output = table(fmt)

    return output

def main():
    print(isis_table("joel"))

if __name__ == "__main__":
    main()
