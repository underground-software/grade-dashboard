#!/bin/env python
import sys, os, email
from datetime import datetime
from common import add_sub

def new_sub(sub_id, user, timestamp, emails):
    tos, frs = [], []
    for e in emails:
        print("EMAIL:", e)
        tos += e['X-KDLP-Orig-To'].split('@')[0]
        frs += e['X-KDLP-Orig-From'].split('@')[0]

    print(f'froms:{str(frs)} tos:{str(tos)}')
    return add_sub(sub_id, user, timestamp)

def main():
    [sub_id, user, timestamp] = sys.argv[1:4]
    log_msg=f'{datetime.fromtimestamp(int(timestamp))} {sub_id} {user}'
    emails=[]
    print(log_msg)
    # iterate over the triggering patchset
    sub_path=f'{os.environ.get("LOG_DIR")}/{sub_id}'
    with open(sub_path, 'r') as sub_file:
        print(f'reading from {sub_path}')
        # write to unconditional submission log
        with open(os.environ.get('SUB_LOG'), 'a') as sub_log_file:
            print(f'writing to {os.environ.get("SUB_LOG")}')
            print(log_msg, file=sub_log_file)
            e = None
            print(f'reading from {sub_path}')
            i=0
            for line in sub_file.readlines():
                # skip first line
                if i < 1:
                    i=i+1
                    continue
                with open(f'{os.environ.get("RAW_DIR")}/{line.strip().split(" ")[0]}', 'r') as mail_file:
                    e = email.message_from_file(mail_file)
                    print(f"GOT AN e: {str(e)}")
                    emails += [e]

    # this function returns TODO
    # to reject the submission, triggering an email notification
    ret = new_sub(sub_id, user, timestamp, emails)

    # we'll do something like this
    if ret is not None:
        with open(os.environ.get('VALID_LOG'), 'a') as valid_sub_log_file:
            print(log_msg, file=valid_sub_log_file)

    return ret

if __name__ == "__main__":
    main()
