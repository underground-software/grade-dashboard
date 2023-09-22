#!/bin/bash


export EDIR=/var/orbit/email_data
export LOGDIR=$EDIR/logs
export SUBLOG=$EDIR/sub.log
export SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $LOGDIR
O=$(test -f "$SUBLOG" && wc -l < "$SUBLOG" || echo "0")
# count subs
N=$(wc -l < <(ls -t))
# get prev or nothing if empty

# count by subtracting handled count
X=$((${N} - ${O}))

new=$(mktemp)
head -n $X <(ls -t) > $new

while read -r subid; do
	time=$(awk 'NR==1 {print $1}' < $LOGDIR/$subid)
	user=$(awk 'NR==1 {print $2}' < $LOGDIR/$subid)
	$SCRIPT_DIR/onsub.py $subid $user $time
done < $new
