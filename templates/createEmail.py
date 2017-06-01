import os
from sys import argv
from distutils.dir_util import copy_tree
from shutil import copyfile
import sys
import subprocess
import emailBuilder
from bbB.bbB import bbB
from BLD.BLD import BLDWeekly
from BLD.BLD import BLDNoHeader
from KF.KF import KFLoyalty
from genericEmail import genericEmail

reload(sys)
sys.setdefaultencoding('utf8')

projectOptions = "1. BuyBuyBaby\n2. BLD Weekly Email\n3. BLD Without Header\n4. KF Loyalty Email\n5. Generic Email"

def printUsageAndExit():
    print("Usage: python createEmail.py <projectNumber> <Name> <CRFFile> [<images directory>]")
    print("Project Number Options:\n" + projectOptions + "\n")
    exit(1)

class setupData:
    def __init__(self, emailData, emailName):
        self.projectName = emailName

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

if len(argv) > 1:
    project = argv[1]
    if len(argv) > 2:
        emailName = argv[2]
        crf_file = argv[3]
        if len(argv) > 4:
            source_images = argv[4]
        else:
            source_images = None
    else:
        printUsageAndExit()
else:
    project = raw_input("Select Project:\n" + projectOptions + "\n")
    emailName = raw_input("Enter Email Name\n")
    crf_file = raw_input("Enter Full Path to CRF File (Drag and Drop)\n")
    source_images = raw_input("Enter Full Path to Images Folder (Drag and Drop)\n")

if str(project).strip() == str(1):
    emailData = bbB()
elif str(project).strip() == str(2):
    emailData = BLDWeekly()
elif str(project).strip() == str(3):
    emailData = BLDNoHeader()
elif str(project).strip() == str(4):
    emailData = KFLoyalty()
elif str(project).strip() == str(5):
    emailData = genericEmail()
else:
    printUsageAndExit()

mySetupData = setupData(emailData, emailName)
emailData.setup(crf_file, mySetupData.imagePath)

for item in [mySetupData.dataPath, mySetupData.sourcePath, mySetupData.imagePath]:
    if not os.path.exists(item):
        os.makedirs(item)

copyfile(emailData.ymlTemplate, mySetupData.ymlPath)
copyfile(emailData.erbTemplate, mySetupData.erbPath)

if source_images is not None and source_images.strip() != "":
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