#!/bin/bash

SVCDIR=/etc/systemd/system
cp ata.path $SVCDIR
cp ata.service $SVCDIR
cp ata-tbreak.service $SVCDIR
cp ata-watchdog.service $SVCDIR

systemctl daemon-reload

# known issues: this complains about wanting to be linked into the system (still works though)
start_if_not_active() { systemctl is-active $1 || systemctl enable --now $1 ; }
start_if_not_active ata.path
start_if_not_active ata-tbreak.service
start_if_not_active ata-watchdog.service

sqlite3 grades.db ".read grades.default" ".exit"
