#!/bin/bash

SVCDIR=/etc/systemd/system
cp ata.path $SVCDIR
cp ata.service $SVCDIR
cp tbreak.service $SVCDIR

systemctl enable --now ata.path

DB_INIT=$(mktemp)
cat < grades.default.pre submissions.default assignments.default grades.default.post > $DB_INIT

sqlite3 grades.db ".read $DB_INIT" ".exit"
