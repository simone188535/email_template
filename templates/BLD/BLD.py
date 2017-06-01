from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuilder import encodeText

class BLDBase(object):
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
            for x in range(0, len(irow) - 1):
                if irow[x].strip() == "Task:":
                    fileContents = fileContents.replace("__EMAIL_NAME__", irow[x + 1])
                    nameFound = True
                elif irow[x].strip() == "Subject Line:":
                    fileContents = fileContents.replace("__TITLE__", irow[x + 1])
                    titleFound = True
                if nameFound and titleFound:
                    break
            if nameFound and titleFound:
                break

        return fileContents

class BLDNoHeaderFooter(BLDBase):
    def __init__(self):
        self.projectNamePrefix = "BLD_"
        self.folderPath = "balduccis"
        self.ymlTemplate = "BLD/BLD_Template_Weekly_Email_053017.yml"
        self.erbTemplate = "BLD/BLD_Template_No_Header_Footer.erb"

        self.sheet = 0
        self.altTextColumn = 2
        self.linkColumn = 5

class BLDWeekly(BLDBase):
    def __init__(self):
        self.projectNamePrefix = "BLD_"
        self.folderPath = "balduccis"
        self.ymlTemplate = "BLD/BLD_Template_Weekly_Email_053017.yml"
        self.erbTemplate = "BLD/BLD_Template_Weekly_Email_053017.erb"

        self.sheet = 0
        self.altTextColumn = 2
        self.linkColumn = 5