#!/bin/bash

export SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPT_DIR/ata.conf

cd $LOG_DIR
O=$(test -f "$SUB_LOG" && wc -l < "$SUB_LOG" || echo "0")
# count subs
N=$(wc -l < <(ls -t))
# get prev or nothing if empty

# count by subtracting  handled count
X=$((${N} - ${O}))

# the first $X lines of $(ls)
# sorted by new to old
# are the $X new patches
# that must be processed
NEW_EMAIL_ID_LIST_TEMP_FILE=$(mktemp)
head -n $X <(ls -t) > $NEW_EMAIL_ID_LIST_TEMP_FILE

provide_patchset() {
 	#patchset_path="$LOG_DIR/$1" > /var/orbit/cano.py/mercury/test.out
	count=$(cat $patchset_path | tail -n +2 | wc -l)
	mkdir -p "$WORK_DIR"
	for ((i=1;i<=$count;++i)); do
			email_id="$(awk -v i=$(($i + 1)) 'NR==i' < $patchset_path)"
			$WEBSERVER_DIR/to_eml.py $RAW_DIR/$email_id $WORK_DIR/$email_id
	done
}

echo "ata found $X new emails"

# handle case of more than one new id
mkdir -p $WORK_DIR
while read -r sub_id; do
	#provide_patchset "$sub_id"
	time=$(awk 'NR==1 {print $1}' < $LOG_DIR/$sub_id)
	user=$(awk 'NR==1 {print $2}' < $LOG_DIR/$sub_id)
	echo "user=$user"
	echo "time=$time"
	echo "sub_id=$sub_id"
	echo "SUB_LOG: $SUB_LOG"

	$SCRIPT_DIR/ata.onsub.py $sub_id $user $time
done < "$NEW_EMAIL_ID_LIST_TEMP_FILE"
#cat $NEW_EMAIL_ID_LIST_TEMP_FILE
rm -f $NEW_EMAIL_ID_LIST_TEMP_FILE
