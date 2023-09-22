#!/bin/bash

# overwritable by env
TBREAK_SECS=${TBREAK_SECS:-10}
die() { echo "error: $1" ; exit 1 ; }

echo "ata taking $TBREAK_SECS second tolerance break"
sleep ${TBREAK_SECS}
echo "ata finishes tbreak"
systemctl restart ata.path

systemctl -q is-active ata.path || die "failed to restart ata.path after tbreak"
systemctl restart ata # this one will exit

echo "ata is ready to roll"
