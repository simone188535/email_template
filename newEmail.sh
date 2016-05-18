#!/bin/bash
if [ $# -ne 3 ]; then
	echo "Usage: newEmail.sh \$template \$client \$project"
    exit 1
fi

# client/project
TEMPLATE=$1
# new client
CLIENT=$2
# new project
PROJECT=$3

if [ ! -d "./source/$TEMPLATE" ]; then
    echo "$TEMPLATE should be a directory."
	exit 1
fi

if [ ! -d "./source/$CLIENT" ]; then
	mkdir ./source/$CLIENT
fi
if [ ! -d "./data/$CLIENT" ]; then
	mkdir ./data/$CLIENT
fi

if [ ! -d "./source/$CLIENT/$PROJECT" ]; then
	mkdir ./source/$CLIENT/$PROJECT
fi
if [ ! -d "./data/$CLIENT/$PROJECT" ]; then
	mkdir ./data/$CLIENT/$PROJECT
fi

scp -r data/$TEMPLATE/* data/$CLIENT/$PROJECT/
scp -r source/$TEMPLATE/* source/$CLIENT/$PROJECT/
mv data/$CLIENT/$PROJECT/*.yml data/$CLIENT/$PROJECT/$PROJECT.yml
mv source/$CLIENT/$PROJECT/*.html.erb source/$CLIENT/$PROJECT/$PROJECT.html.erb
mv source/$CLIENT/$PROJECT/*.txt.erb source/$CLIENT/$PROJECT/$PROJECT.txt.erb