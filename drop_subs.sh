#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR



sqlite3 grades.db <<EOF
DROP TABLE submissions;
DROP TABLE assignments;
EOF

$SCRIPT_DIR/setup.sh
