import os
import re
from createEmail import generateEmail
from shutil import rmtree

projects = {"buybuybaby":"1", "sprichards":6}

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def buildDirectory(directory, project):
    searchLocation = "autobuild/{}".format(directory)
    folders = get_immediate_subdirectories(searchLocation)
    for folder in folders:
        excelFile = None
        images = None

        for file in os.listdir(os.path.join(searchLocation,folder)):
            regPattern = re.compile(".*\.(xls|xlsx)")
            if file == "images":
                images = os.path.abspath(os.path.join(searchLocation, folder, file))
            elif regPattern.match(file) is not None:
                excelFile = os.path.abspath(os.path.join(searchLocation, folder, file))

        if excelFile is not None and images is not None:
            generateEmail(project=project, crf_file=excelFile, source_images=images, emailName=folder)

            rmtree(os.path.join(searchLocation,folder))


for project in projects:
    buildDirectory(project, projects[project])