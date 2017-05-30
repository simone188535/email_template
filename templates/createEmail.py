import os
from sys import argv
from distutils.dir_util import copy_tree
from shutil import copyfile
import sys
import subprocess
import emailBuilder
from bbB.bbB import bbB
from BLD.BLD import BLD
from genericEmail import genericEmail

reload(sys)
sys.setdefaultencoding('utf8')

class setupData:
    def __init__(self, emailData, date, emailName):
        self.projectName = emailData.projectNamePrefix + date + "_" + emailName

        fullPath = os.path.abspath(os.getcwd())
        if "emails" in fullPath:
            fullPath = "emails".join(fullPath.split("emails")[:-1]) + "emails"
        else:
            raise SyntaxError("Unable to find emails repository, are you running this script from inside the emails repo?")

        self.dataPath =  fullPath + "/data/" + emailData.folderPath + "/" + self.projectName
        self.sourcePath = fullPath + "/source/" + emailData.folderPath + "/" + self.projectName
        self.imagePath = self.sourcePath + "/images"
        self.erbPath = self.sourcePath + "/" + self.projectName + ".html.erb"
        self.ymlPath = self.dataPath + "/" + self.projectName + ".yml"

if (len(argv) > 1):
    project = argv[1]
    emailName=argv[2]
    date=argv[3]
    crf_file=argv[4]
    source_images=argv[5]
else:
    project = raw_input("Select Project:\n1. BuyBuyBaby\n2. BLD\n3. Other\n")
    emailName = raw_input("Enter Email Name\n")
    date = raw_input("Enter Email Date (MMDDYY)\n")
    crf_file = raw_input("Enter Full Path to CRF File (Drag and Drop)\n")
    source_images = raw_input("Enter Full Path to Images Folder (Drag and Drop)\n")

if str(project).strip() == str(1):
    emailData = bbB()
elif str(project).strip() == str(2):
    emailData = BLD()
else:
    emailData = genericEmail()

mySetupData = setupData(emailData, date, emailName)
emailData.setup(crf_file, mySetupData.imagePath)

for item in [mySetupData.dataPath, mySetupData.sourcePath, mySetupData.imagePath]:
    if not os.path.exists(item):
        os.makedirs(item)

copyfile(emailData.ymlTemplate, mySetupData.ymlPath)
copyfile(emailData.erbTemplate, mySetupData.erbPath)

copy_tree(source_images, mySetupData.imagePath)

erbFile = open(mySetupData.erbPath, "r")
erbLines = erbFile.readlines()
erbFile.close()

erbContents = ""
for erbLine in erbLines:
    erbContents += erbLine
erbContents = erbContents.replace("__PROJECT_NAME__", mySetupData.projectName)
erbFile = open(mySetupData.erbPath, "w")
erbFile.write(erbContents)
erbFile.close()

builder = emailBuilder.emailBuilder(mySetupData.ymlPath, crf_file, mySetupData.imagePath, emailData.sheet, emailData.altTextColumn, emailData.linkColumn)
builder.createEmail(emailData)

subprocess.call("bundle exec middleman build", shell=True)
subprocess.call("grunt build", shell=True)