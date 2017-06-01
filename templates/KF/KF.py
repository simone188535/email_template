from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuilder import encodeText

class KFLoyalty(object):
    def __init__(self):
        self.projectNamePrefix = "KF_"
        self.folderPath = "kingsfoodmarkets"
        self.ymlTemplate = "KF/KF_Template_Loyalty_Email_053117.yml"
        self.erbTemplate = "KF/KF_Template_Loyalty_Email_053117.erb"

        self.sheet = 0
        self.altTextColumn = 2
        self.linkColumn = 5

    def setup(self, crf_file, imagePath):
        pass

    def update(self, fileContents, sheet):
        fileContents = self.updateHeader(fileContents, sheet)
        return fileContents

    def updateHeader(self, fileContents, sheet):
        # find and update title
        nameFound = False
        titleFound = False

        for irow in sheet.rows():
            for x in range(0, len(irow) -1):
                if irow[x].strip() == "Task:":
                    fileContents = fileContents.replace("__EMAIL_NAME__", irow[x+1])
                    nameFound = True
                elif irow[x].strip() == "Subject:":
                    fileContents = fileContents.replace("__TITLE__", irow[x+1])
                    titleFound = True
                if nameFound and titleFound:
                    break
            if nameFound and titleFound:
                break

        return fileContents