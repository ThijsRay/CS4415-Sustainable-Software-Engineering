#!/usr/bin/env bash

# Test results in csv
# Shuffle option
# Cooldown between tests
# Save username to run the browser without super user privileges

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

# Set magic variables for current file & dir
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__root="$(cd "$(dirname "${__dir}")" && pwd)"

USER=$(whoami)
DATE=$(date +"%s")

source venv/bin/activate
export PATH=$PATH:$(pwd)

#Change the for loop to increase the amount of iterations
for i in {0..14}
do
    mkdir -p "$__dir/results"
    SUBDIR="$__dir/results/$DATE-$i"
    mkdir "$SUBDIR"
    while read -r CMD; do
        FILENAME=`echo $CMD | cut -d ' ' -f3,4 --output-delimiter='_'`
        echo "Running test $FILENAME iteration $i"
        sudo ./jouleit.sh -l >> "$SUBDIR/$FILENAME"
        sudo -E ./jouleit.sh -c "sudo -E -u $USER -- $CMD" >> "$SUBDIR/$FILENAME"
    done < <(cat "$__dir/.cmds/with_adblock" "$__dir/.cmds/without_adblock" | sort -R) # Get all commands and shuffle them
done
