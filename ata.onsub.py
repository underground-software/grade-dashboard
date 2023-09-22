#!/bin/env python
import sys, os, email
from datetime import datetime
from common import add_sub

def new_sub(sub_id, user, timestamp, emails):
    tos, frs = [], []
    for e in emails:
        tos += em['X-KDLP-Orig-To'].split('@')[0]
        frs += em['X-KDLP-Orig-From'].split('@')[0]
    return add_sub(sub_id, user, timestamp)

def main(LOG):
    [sub_id, user, timestamp] = sys.argv[1:4]
    log_msg=f'{datetime.fromtimestamp(int(timestamp))} {sub_id} {user}'
    emails=[]
    LOG(log_msg)
    # iterate over the triggering patchset
    with open(f'{os.environ.get("LOG_DIR")}/{sub_id}', 'r') as mail_file:
        # write to unconditional submission log
        with open(os.environ.get('SUB_LOG'), 'a') as sub_log_file:
            LOG(f'writing to {os.environ.get("SUB_LOG")}')
            print(log_msg, file=sub_log_file)
            em = None
            for line in mail_file.readlines():
                # skip first line
                if em is not None:
                    em = email.message_from_file(line.strip())
                    emails += em
                
            

    # this function returns TODO
    # to reject the submission, triggering an email notification
    ret = new_sub(sub_id, user, timestamp, emails )

    with open(os.environ.get('VALID_LOG'), 'a') as valid_sub_log_file:
        print(log_msg, file=valid_sub_log_file)
        
    return ret

if __name__ == "__main__":
    print(f'args: {str(sys.argv)}', file=sys.stderr)
    with open(os.environ.get('ATA_LOG'), 'a') as ata_log_file:
         main(lambda msg: print(msg, file=ata_log_file))
