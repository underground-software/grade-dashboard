#!/bin/bash

sqlite3 grades.db <<EOF
DROP TABLE submissions;
EOF

sqlite3 grades.db < grades.default
