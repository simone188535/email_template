from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuildClass import emailBuilder
# Needed for automatically sending tests in Mailchimp
#import mailChimp
#import os

class OTPBuilder(emailBuilder):
    def __init__(self, crf_file, source_images, emailName):
        self.projectNamePrefix = "OTP_"
        self.folderPath = "otp"
        self.ymlTemplate = "OTP/OTP_Template_091418.yml"
        self.erbTemplate = "OTP/OTP_Template_091418.erb"

        self.sheetName = 0
        self.altTextColumn = 2 # Column numbers starting from 0
        self.linkColumn = 5

        super(OTPBuilder, self).__init__(**kwargs)

    def update(self):
        self.updateHeader()

	def updateHeader(self):
        # find and update title
        nameFound = False
        titleFound = False
        preheaderFound = False

        for irow in self.sheet.rows():
            for x in range(0, len(irow) -1):
                if irow[x].strip() == "Task:":
                    self.fileContents = self.fileContents.replace("__EMAIL_NAME__", irow[x+1])
                    nameFound = True
                elif irow[x].strip() == "Subject Line:":
                    self.fileContents = self.fileContents.replace("__TITLE__", irow[x+1])
                    titleFound = True
                elif irow[x].strip() == "Pre-header:":
                    self.fileContents = self.fileContents.replace("__PREHEADER__", irow[x+1])
                    preheaderFound = True
                if nameFound and titleFound:
                    break
            if nameFound and titleFound:
                break

        # More work needed here...See (defunct) bbB.py file for an example


    def loadData(self):
        super(KFLoyalty, self).loadData()
        self.layoutSheetName = "Layout"
        self.layoutsheet = self.workbook.sheet_by_name(self.layoutSheetName)

    def generateYmlContent(self):
    	# Do we need to hook into this to adjust how the images are found and pulled in? See KF.py for reference.
