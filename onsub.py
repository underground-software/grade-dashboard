#!/bin/env python

import sys, os
from datetime import datetime
from common import add_sub

SUBID=sys.argv[1]
USER=sys.argv[2]
TIME=sys.argv[3]


with open(os.environ.get('SUBLOG'), 'a') as f:
    print(f'{datetime.fromtimestamp(int(TIME))} {SUBID} {USER}', file=f)
add_sub(SUBID, USER, TIME)
