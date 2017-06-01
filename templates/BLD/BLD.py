from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuilder import encodeText

class BLD(object):
    def __init__(self):
        self.projectNamePrefix = "BLD_"
        self.folderPath = "balduccis"
        self.ymlTemplate = "BLD/BLD_Template_053017.yml"
        self.erbTemplate = "BLD/BLD_Template_053017.erb"

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
        for irow in sheet.rows():
            if irow[0] == "Task:":
                fileContents = fileContents.replace("__EMAIL_NAME__", irow[1])
                break

        return fileContents