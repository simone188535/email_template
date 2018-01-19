from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuildClass import emailBuilder
import mailChimp
import os

class bbBBuilder(emailBuilder):
    def __init__(self, **kwargs):
        self.projectNamePrefix = "bbB_"
        self.folderPath = "buybuyBaby"
        self.ymlTemplate = "bbB/bbB_Template_05012017.yml"
        self.erbTemplate = "bbB/bbB_Template_05012017.erb"
        super(bbBBuilder, self).__init__(**kwargs)
        self.imageRows = []
        self.bodyCounter = 0
        self.sendEmail = False
        if "sendEmail" in kwargs:
            sendEmail = kwargs["sendEmail"]
            if str(sendEmail).strip().upper() == 'TRUE':
                self.sendEmail = True


    def loadData(self):
        copy_tree("bbB/social_images", self.imagePath)

        if "CANADA" in self.crf_file.upper():
            copy_tree("bbB/CA_images", self.imagePath)
            self.sheetName = "ASF"
            self.altTextColumn = 2
            self.linkColumn = 5
            self.locationColumn = 1
            self.canada = True
        else:
            copy_tree("bbB/US_images", self.imagePath)
            self.sheetName = "Link Table"
            self.altTextColumn = 1
            self.linkColumn = 4
            self.locationColumn = 0
            self.canada = False
        super(bbBBuilder, self).loadData()

    def findImageRow(self, image):
        if len(self.imageRows) < 1:
            for irow in self.sheet.rows():
                if irow[self.locationColumn].strip() == 'Body' and irow[self.linkColumn].strip() != '':
                    self.imageRows.append(irow)
        row = self.imageRows[self.bodyCounter]
        self.bodyCounter = self.bodyCounter + 1
        return row

    def update(self):
        self.updateHeader()

    def updateNavBar(self, row, navBarCount):
        self.fileContents = self.fileContents.replace("__NAV" + str(navBarCount) + "_ALT__", self.encodeText(row[self.altTextColumn]))
        self.fileContents = self.fileContents.replace("__NAV" + str(navBarCount) + "_LINK__", self.encodeText(row[self.linkColumn]))
        navBarCount += 1

        return navBarCount, self.fileContents

    def updateSubHeader(self, row):
        altText = row[self.altTextColumn]
        if altText == "View as a web page":
            self.fileContents = self.fileContents.replace("__WEBPAGE_LINK__", row[self.linkColumn])
        elif altText == "buybuy Baby Logo" or row[self.altTextColumn] == "buybuy Canada Baby Logo":
            self.fileContents = self.fileContents.replace("__LOGO_LINK__", row[self.linkColumn])
            self.fileContents = self.fileContents.replace("__LOGO_ALT__", self.encodeText(row[self.altTextColumn]))
        elif "FREE SHIPPING ON ORDERS OVER $49" in altText.upper():
            self.fileContents = self.fileContents.replace("__FREE_SHIPPING_LINK__", row[self.linkColumn])
        elif "IN-STORE PICKUP" in altText.upper():
            self.fileContents = self.fileContents.replace("__INSTORE_LINK__", row[self.linkColumn])
        elif altText == "baby registry logo":
            self.fileContents = self.fileContents.replace("__REGISTRY_LINK__", row[self.linkColumn])

        return self.fileContents

    def updateHeader(self):
        # find and update title
        for irow in self.sheet.rows():
            if irow[self.locationColumn] == "Sub-header":
                self.fileContents = self.fileContents.replace("__EMAIL_TITLE__", self.encodeText(irow[self.altTextColumn]))
                self.fileContents = self.fileContents.replace("__EMAIL_TITLE_LINK__", irow[self.linkColumn])
                break

        navBarCount = 1

        for irow2 in self.sheet.rows():
            if irow2[self.locationColumn] == "Sub-header":
                self.fileContents = self.updateSubHeader(irow2)
            elif irow2[self.locationColumn] == "Header Bar":
                navBarCount, self.fileContents = self.updateNavBar(irow2, navBarCount)

        if (self.canada):
            self.fileContents = self.fileContents.replace("__LOGO_IMAGE__", "bbB_emailheader_Logo_CA.jpg")
            self.fileContents = self.fileContents.replace("__FREE_SHIPPING_IMAGE__", "bbB_emailheader_FreeShipping_CA.jpg")
            self.fileContents = self.fileContents.replace("__INSTORE_IMAGE__", "bbB_emailheader_InStore_CA.jpg")
            self.fileContents = self.fileContents.replace("__REGISTRY_IMAGE__", "bbB_emailheader_RegistryLogo_CA.jpg")
            self.fileContents = self.fileContents.replace("__NAV1_IMAGE__", "bbB_emailheader_NAV1_CA.jpg")
            self.fileContents = self.fileContents.replace("__NAV2_IMAGE__", "bbB_emailheader_NAV2_CA.jpg")
            self.fileContents = self.fileContents.replace("__NAV3_IMAGE__", "bbB_emailheader_NAV3_CA.jpg")
        else:
            self.fileContents = self.fileContents.replace("__LOGO_IMAGE__", "bbB_emailheader_Logo.jpg")
            self.fileContents = self.fileContents.replace("__FREE_SHIPPING_IMAGE__", "bbB_emailheader_FreeShipping.jpg")
            self.fileContents = self.fileContents.replace("__INSTORE_IMAGE__", "bbB_emailheader_InStore.jpg")
            self.fileContents = self.fileContents.replace("__REGISTRY_IMAGE__", "bbB_emailheader_RegistryLogo.jpg")
            self.fileContents = self.fileContents.replace("__NAV1_IMAGE__", "bbB_emailheader_NAV1.jpg")
            self.fileContents = self.fileContents.replace("__NAV2_IMAGE__", "bbB_emailheader_NAV2.jpg")
            self.fileContents = self.fileContents.replace("__NAV3_IMAGE__", "bbB_emailheader_NAV3.jpg")

        return self.fileContents

    def postProcess(self, **kwargs):
        for irow in self.sheet.rows():
            if irow[self.locationColumn].strip() == 'Sub-header' and irow[self.altTextColumn].strip() != '':
                subject_line = irow[self.altTextColumn]
                break


        #recipients = ["richard.hines@purered.net"]
        recipients = ["110215SPR@litmustest.com", "devpurered.runme@previews.emailonacid.com", "qa@purered.net"]

        if self.sendEmail and os.path.isfile("{}/{}.html".format(self.prodPath, self.projectName)):
            mailChimp.upload(self.prodPath, self.projectName, subject_line, "dev@purered.net", "Pure Red", recipients)