#!/bin/bash

export EDIR=/var/orbit/email_data
export WSDIR=/var/orbit/webservers
export LOGDIR=$EDIR/logs
export SUBLOG=$EDIR/sub.log
export RAWDIR=$EDIR/mail
export WORKDIR=$EDIR/mail_ready
export SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $LOGDIR
O=$(test -f "$SUBLOG" && wc -l < "$SUBLOG" || echo "0")
# count subs
N=$(wc -l < <(ls -t))
# get prev or nothing if empty

# count by subtracting  handled count
X=$((${N} - ${O}))

# the first $X lines of $(ls)
# sorted by new to old
# are the $X new patches
# that must be processed
new=$(mktemp)
head -n $X <(ls -t) > $new

provide_patchset() {
 	patchset_path="$LOGDIR/$1" > /var/orbit/cano.py/mercury/test.out
	echo "PATHCHSET_PATH $patchset_path"
	count=$(cat $patchset_path | tail -n +2 | wc -l)
	mkdir -p "$WORKDIR"
	for ((i=1;i<=$count;++i)); do
			email_id="$(awk -v i=$(($i + 1)) 'NR==i' < $patchset_path)"
			echo "email id: $email_id"
			$WSDIR/to_eml.py $RAWDIR/$email_id $WORKDIR/$email_id
	done
}

# handle case of more than one new id
mkdir -p $WORKDIR
while read -r subid; do
	provide_patchset "$subid"
	time=$(awk 'NR==1 {print $1}' < $LOGDIR/$subid)
	user=$(awk 'NR==1 {print $2}' < $LOGDIR/$subid)
	$SCRIPT_DIR/onsub.py $subid $user $time
done < $new
rm -f $new
