from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuilder import encodeText

class bbB(object):
    def __init__(self):
        self.projectNamePrefix = "bbB_"
        self.folderPath = "buybuyBaby"
        self.ymlTemplate = "bbB/bbB_Template_05012017.yml"
        self.erbTemplate = "bbB/bbB_Template_05012017.erb"

        copy_tree("bbB/social_images", imagePath)

    def setup(self, crf_file, imagePath):
        if "CANADA" in crf_file.upper():
            copy_tree("bbB/CA_images", imagePath)
            self.sheet = "ASF"
            self.altTextColumn = 2
            self.linkColumn = 5
            self.locationColumn = 1
        else:
            copy_tree("bbB/US_images", imagePath)
            self.sheet = "Link Table"
            self.altTextColumn = 1
            self.linkColumn = 4
            self.locationColumn = 0

    def update(self, fileContents, sheet):
        fileContents = self.updateHeader(fileContents, sheet)
        return fileContents

    def updateHeader(self, fileContents, sheet):
        # find and update title
        for irow in sheet.rows():
            if irow[self.locationColumn] == "Sub-header":
                fileContents = fileContents.replace("__EMAIL_TITLE__", encodeText(irow[self.altTextColumn]))
                fileContents = fileContents.replace("__EMAIL_TITLE_LINK__", irow[self.linkColumn])
                break

        return fileContents