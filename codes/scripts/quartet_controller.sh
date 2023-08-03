#!/bin/sh

# pwd
cd  "$3"

sh quartet_count.sh $1 | perl summarize_quartets_stdin.pl > $2

cd - > /dev/null

# pwd