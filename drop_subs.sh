#!/bin/bash

sqlite3 grades.db <<EOF
DROP TABLE submissions;
EOF

DB_INIT=$(mktemp)
cat < $(cat grades.db.recipe) > $DB_INIT

sqlite3 grades.db ".read $DB_INIT" ".exit"
