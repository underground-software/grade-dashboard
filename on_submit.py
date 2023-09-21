#!/bin/env python

from datetime import datetime

with open('submission.log', 'a+') as f:
    print(str(datetime.utcnow()), file=f)
