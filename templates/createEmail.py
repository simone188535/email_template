import os
from sys import argv
from distutils.dir_util import copy_tree
from shutil import copyfile
import sys
import subprocess
from bbB.bbB import bbBBuilder
from BLD.BLD import BLDWeekly
from BLD.BLD import BLDNoHeaderFooter
from KF.KF import KFLoyalty
from SPR.SPR import SPRBuilder
from genericEmail import genericEmailBuilder

reload(sys)
sys.setdefaultencoding('utf8')

class generateEmail(object):
    def __init__(self, **kwargs):
        if "project" in kwargs:
            project = kwargs["project"]
        if "crf_file" in kwargs:
            crf_file = kwargs["crf_file"]
        if "source_images" in kwargs:
            source_images = kwargs["source_images"]
        if "emailName" in kwargs:
            emailName = kwargs["emailName"]


        if str(project).strip() == str(1):
            builder = bbBBuilder(**kwargs)
        elif str(project).strip() == str(2):
            builder = BLDWeekly(**kwargs)
        elif str(project).strip() == str(3):
            builder = BLDNoHeaderFooter(**kwargs)
        elif str(project).strip() == str(4):
            builder = KFLoyalty(**kwargs)
        elif str(project).strip() == str(5):
            builder = genericEmailBuilder(**kwargs)
        elif str(project).strip() == str(6):
            builder = SPRBuilder(**kwargs)
        else:
            printUsageAndExit()

        for item in [builder.dataPath, builder.sourcePath, builder.imagePath]:
            if not os.path.exists(item):
                os.makedirs(item)

        builder.setupTemplates()
        builder.copySourceFiles(source_images)
        builder.createEmail()

        subprocess.call("bundle exec middleman build", shell=True)
        subprocess.call("grunt build", shell=True)

        builder.postProcess()


projectOptions = "1. BuyBuyBaby\n2. BLD Weekly Email\n3. BLD Simple\n4. KF Loyalty Email\n5. Generic Email\n6. SPR"


def printUsageAndExit():
    print("Usage: python createEmail.py <projectNumber> <Name> <CRFFile> [<images directory>]")
    print("Project Number Options:\n" + projectOptions + "\n")
    exit(1)


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

    generateEmail(project=project, crf_file=crf_file, source_images=source_images, emailName=emailName)