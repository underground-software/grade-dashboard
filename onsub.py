#!/bin/env python

import sys, os, email
from datetime import datetime
from common import add_sub


def main():
    sub_id, user, timestamp = 
sub_id=sys.argv[1]
user=sys.argv[2]
timestamp=sys.argv[3]
    with open(os.environ.get('RAWDIR') + sub_id, 'r') as mail_file
        em = email.message_from_from_file(mail_file)
        to = em['X-KDLP-Orig-To'].split('@')[0]
        fr = em['X-KDLP-Orig-From'].split('@')[0]
        with open(os.environ.get('SUBLOG'), 'a') as sub_log:
            print(f'{datetime.fromtimestamp(int(timestamp))} {sub_id} {user}', file=sub_log)

    new_sub(sub_id, user, timestamp, fr )

if __name__ == "__main__":
    main()
