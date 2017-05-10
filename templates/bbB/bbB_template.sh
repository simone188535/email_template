#!/bin/bash

if [ $# -lt 1 ]
then
echo "Enter project name (E.x. 'WeekendDeals', 'ProjectNursery'):"
read projName_sub

echo "Enter Email Date (DDMMYYYY):"
read date

echo "Enter CRF file (with full path):"
read crf_file

echo "Enter path to images:"
read source_images

echo "Enter title:"
read title

echo "Enter title link:"
read link

echo
else
if [ $1 -eq "--help" ]
then
echo "Usage: bbB_template.sh \"ProjectName\" Date CRF_Path Image_Path Image_Pattern Title Title_Link"
else
projName_sub=$1
date=$2
crf_file=$3
source_images=$4
title=$5
link=$6
fi
fi

projectName="bbB_${date}_${projName_sub}"
image_pattern=$projectName"_"
dataPath="../../data/buybuyBaby/$projectName"
sourcePath="../../source/buybuyBaby/$projectName"
imagePath="$sourcePath/images"
erbFile="$sourcePath/$projectName.html.erb"

#Template file and directory creation
mkdir -p $dataPath
cp bbB_Template_05012017.yml $dataPath/$projectName.yml
mkdir -p $sourcePath
cp bbB_Template_05012017.erb $erbFile
mkdir -p $imagePath
cp -R image_templates/* $imagePath

#ERB file template entries
sed 's/__PROJECT_NAME/'"$projectName"'/g' $erbFile > tmp
mv tmp $erbFile

#YML file template entries
sed 's/__EMAIL_TITLE_LINK/'"$(echo $link | sed -e 's/\\/\\\\/g; s/\//\\\//g; s/&/\\\&/g')"'/g' $dataPath/$projectName.yml > tmp
mv tmp $dataPath/$projectName.yml
sed 's/__EMAIL_TITLE/'"$title"'/g' $dataPath/$projectName.yml > tmp
mv tmp $dataPath/$projectName.yml

for f in $source_images/*
do
    cp $f $imagePath
done

python bbB_template.py $dataPath/$projectName.yml $crf_file $image_pattern

#mkdir -p $imagePath/templates
#cp -r image_templates/* $imagePath/templates