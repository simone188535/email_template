import os
from sys import argv
from distutils.dir_util import copy_tree
from shutil import copyfile
from shutil import rmtree
import sys
import subprocess
from bbB.bbB import bbBBuilder
from BLD.BLD import BLDWeekly
from BLD.BLD import BLDNoHeaderFooter
from KF.KF import KFLoyalty
from KF.KF import KFGeneric
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


        if str(project).strip().upper() == "BBB":
            builder = bbBBuilder(**kwargs)
        elif str(project).strip().upper() == "BLDWEEKLY":
            builder = BLDWeekly(**kwargs)
        elif str(project).strip().upper() == "BLDSIMPLE":
            builder = BLDNoHeaderFooter(**kwargs)
        elif str(project).strip().upper() == "KFLOYALTY":
            builder = KFLoyalty(**kwargs)
        elif str(project).strip().upper() == "KF":
            builder = KFGeneric(**kwargs)
        elif str(project).strip().upper() == "GENERIC":
            builder = genericEmailBuilder(**kwargs)
        elif str(project).strip().upper() == "SPR":
            builder = SPRBuilder(**kwargs)
        else:
            printUsageAndExit()

        for item in [builder.dataPath, builder.sourcePath, builder.imagePath]:
            if os.path.exists(item):
                rmtree(item, ignore_errors=True)
            os.makedirs(item)

        builder.setupTemplates()
        builder.copySourceFiles(source_images)
        builder.createEmail()

        subprocess.call("bundle exec middleman build", shell=True)
        subprocess.call("grunt build", shell=True)

        builder.postProcess()


projectOptions = {"BBB":"BuyBuyBaby", "BLDWeekly":"BLD Weekly Email", "BLDSimple":"BLD Simple", "KFLoyalty":"KF Loyalty Email", "KF":"KF Generic Email", "Generic":"Generic Email", "SPR":"SP Richards Email"}


def printUsageAndExit():
    print("Usage: python createEmail.py <project> <Name> <CRFFile> [<images directory>]")
    print("Project Options:")
    for item in projectOptions:
        print("\t" + item + ": " + projectOptions[item])
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