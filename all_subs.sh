#!/bin/bash

sqlite3 grades.db <<EOF
SELECT * FROM submissions;
EOF
