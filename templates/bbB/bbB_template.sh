#!/bin/bash

if [ $# -lt 1 ]
then
echo "Enter project name (E.x. 'WeekendDeals', 'ProjectNursery'):"
read projName_sub

echo "Enter Email Date (DDMMYYYY):"
read date

echo "Enter CRF or ASF file (Drag and Drop to terminal):"
read crf_file

echo "Enter path to images (Drag and Drop to terminal):"
read source_images

echo
else
if [ $1 == "--help" ]
then
echo "Usage: bbB_template.sh \"ProjectName\" Date CRF_Path Image_Path Image_Pattern Title Title_Link"
else
projName_sub=$1
date=$2
crf_file=$3
source_images=$4
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
cp -R social_images/* $imagePath

if [[ "$crf_file" =~ "CANADA" ]]
then
    cp -R CA_images/* $imagePath
else
    cp -R US_images/* $imagePath
fi

#ERB file template entries
sed 's/__PROJECT_NAME/'"$projectName"'/g' $erbFile > tmp
mv tmp $erbFile

for f in $source_images/*
do
    cp $f $imagePath
done

python bbB_template.py $dataPath/$projectName.yml $crf_file $source_images

#mkdir -p $imagePath/templates
#cp -r image_templates/* $imagePath/templates