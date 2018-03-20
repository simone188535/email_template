#!/bin/bash
if [ $# -ne 3 ]; then
	echo "Usage: newEmail.sh \$template \$client \$project"
	echo "\$template should be an existing directory in the form 'client_name/project_name' (no quotes)."
    exit 1
fi

# client/project
TEMPLATE=$1
# new client
CLIENT=$2
# new project
PROJECT=$3

# $TEMPLATE specifies a client and project to clone from
# replace '/' in $TEMPLATE with an empty space
# the outer parentheses cause bash to interpret the space-separated string as an array
PARTS=(${TEMPLATE//\// })


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

# text emails are no longer needed
#mv source/$CLIENT/$PROJECT/*.txt.erb source/$CLIENT/$PROJECT/$PROJECT.txt.erb

# replace the client and project names in the files we cloned with the correct values
# NOTE: the '' after -i which is needed for sed on OSX!

# replace old_project name
sed -i '' "s/${PARTS[1]}/${PROJECT}/g" "data/${CLIENT}/${PROJECT}/${PROJECT}.yml"
sed -i '' "s/${PARTS[1]}/${PROJECT}/g" "source/${CLIENT}/${PROJECT}/${PROJECT}.html.erb"
# replace old_client_name in ERB
sed -i '' "s/data\.${PARTS[0]}\.${PARTS[1]}/data.${CLIENT}.${PROJECT}/g" "source/${CLIENT}/${PROJECT}/${PROJECT}.html.erb"
