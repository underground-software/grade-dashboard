#!/bin/bash

SVCDIR=/etc/systemd/system
cp ata.path $SVCDIR
cp ata.service $SVCDIR
cp tbreak.service $SVCDIR

systemctl enable --now ata.path

sqlite3 grades.db ".read grades.default" ".exit"
