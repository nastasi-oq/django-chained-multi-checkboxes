#!/bin/bash
IFS='
'
FOUT="../fixtures/initial_data.json"
nfix="$(ls [0-9][0-9]* | wc -l)"
ct=0
for i in $(ls [0-9][0-9]*); do
    if [ $ct -eq 0 ]; then
        echo "begin  $i" >&2
        ( head -n -2 "$i" ; echo "}," ) > "$FOUT"
    elif [ $ct -eq $((nfix - 1)) ]; then
        echo "end    $i" >&2
        tail -n +2 "$i" >> "$FOUT"
    else
        echo "middle $i" >&2
        ( tail -n +2 "$i" | head -n -2 ; echo "}," ) >> "$FOUT"
    fi
    ct=$((ct + 1))
done
