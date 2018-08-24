from distutils.dir_util import copy_tree
from shutil import copyfile
import pyexcel as p
from emailBuildClass import emailBuilder
import mailChimp
import os

class OTPBuilder(emailBuilder):
    def __init__(self, **kwargs):
        self.projectNamePrefix = "OTP_"
        self.folderPath = "otp"
        self.sheetName = 0
        self.ymlTemplate = "OTP/OTP_Template_080318_Email.yml"
        self.erbTemplate = "OTP/OTP_Template_080318_Email.erb"
        super(OTPBuilder, self).__init__(**kwargs)
        self.imageRows = []
        self.bodyCounter = 0
        self.sendEmail = False
        if "sendEmail" in kwargs:
            sendEmail = kwargs["sendEmail"]
            if str(sendEmail).strip().upper() == 'TRUE':
                self.sendEmail = True

    # Use this to load the footer images if those are being pulled from a folder instead of being in the template

    def loadData(self):
        #self.sheetName = "Link Table"
        self.altTextColumn = 2
        self.linkColumn = 5
        self.locationColumn = 0
        super(OTPBuilder, self).loadData()

    # def findImageRow(self, image):
    #     if len(self.imageRows) < 1:
    #         for irow in self.sheet.rows():
    #             if irow[self.locationColumn].strip() == 'Body' and irow[self.linkColumn].strip() != '':
    #                 self.imageRows.append(irow)
    #     row = self.imageRows[self.bodyCounter]
    #     self.bodyCounter = self.bodyCounter + 1

    #     return row

    def generateImage(self, images):
        articleType = "table"

        table = []

        for image in images:
            imgData = ['']*6

            row = self.findImageRow(image)

            path, imageName = self.getImageRelativePathAndName(image)

            imgData[0] = "image"
            imgData[1] = str(path + imageName).encode('ascii','ignore')
            imgData[2] = self.getImageLink(row[self.linkColumn]).encode('ascii','ignore')
            imgData[5] = self.encodeText(row[self.altTextColumn].encode('ascii','ignore'))

            imgData = self.addAdditionalFields(image, imgData)

            table.append(imgData)

        self.contents.insert(self.insertRow(), "- type: '" + articleType + "'" + self.newLine)
        self.contents.insert(self.insertRow(), "  data: " + str(table) + "" + self.newLine)
        self.contents.insert(self.insertRow(), self.newLine)

    def generateYmlContent(self):
        for irow in self.layoutsheet.rows():
            while '' in irow:
                irow.remove('')
            self.generateImage(irow)

    def update(self):
        self.updateHeader()

    def updateNavBar(self, row, navBarCount):
        self.fileContents = self.fileContents.replace("__NAV" + str(navBarCount) + "_ALT__", self.encodeText(row[self.altTextColumn]))
        self.fileContents = self.fileContents.replace("__NAV" + str(navBarCount) + "_LINK__", self.encodeText(row[self.linkColumn]))
        navBarCount += 1

        return navBarCount, self.fileContents

    ##Could still be useful if header wasn't handled by the template the way it is now.

    # def updateSubHeader(self, row):
    #     altText = row[self.altTextColumn]
    #     if altText == "View as a web page":
    #         self.fileContents = self.fileContents.replace("__WEBPAGE_LINK__", row[self.linkColumn])
    #     elif altText == "buybuy Baby Logo" or row[self.altTextColumn] == "buybuy Canada Baby Logo":
    #         self.fileContents = self.fileContents.replace("__LOGO_LINK__", row[self.linkColumn])
    #         self.fileContents = self.fileContents.replace("__LOGO_ALT__", self.encodeText(row[self.altTextColumn]))
    #     elif "FREE SHIPPING ON ORDERS OVER $49" in altText.upper():
    #         self.fileContents = self.fileContents.replace("__FREE_SHIPPING_LINK__", row[self.linkColumn])
    #     elif "IN-STORE PICKUP" in altText.upper():
    #         self.fileContents = self.fileContents.replace("__INSTORE_LINK__", row[self.linkColumn])
    #     elif altText == "baby registry logo":
    #         self.fileContents = self.fileContents.replace("__REGISTRY_LINK__", row[self.linkColumn])

    #     return self.fileContents

    def updateHeader(self):
        # find and update title
        for irow in self.sheet.rows():
            if irow[self.locationColumn] == "Sub-header":
                self.fileContents = self.fileContents.replace("__EMAIL_TITLE__", self.encodeText(irow[self.altTextColumn]))
                self.fileContents = self.fileContents.replace("__EMAIL_TITLE_LINK__", irow[self.linkColumn])
                break

        ## Adjust for OTP footer images; currently handled by template, but this would be a good feature

        # navBarCount = 1

        # for irow2 in self.sheet.rows():
        #     if irow2[self.locationColumn] == "Sub-header":
        #         self.fileContents = self.updateSubHeader(irow2)
        #     elif irow2[self.locationColumn] == "Header Bar":
        #         navBarCount, self.fileContents = self.updateNavBar(irow2, navBarCount)

        # if (self.canada):
        #     self.fileContents = self.fileContents.replace("__LOGO_IMAGE__", "OTP_emailheader_Logo_CA.jpg")
        #     self.fileContents = self.fileContents.replace("__FREE_SHIPPING_IMAGE__", "OTP_emailheader_FreeShipping_CA.jpg")
        #     self.fileContents = self.fileContents.replace("__INSTORE_IMAGE__", "OTP_emailheader_InStore_CA.jpg")
        #     self.fileContents = self.fileContents.replace("__REGISTRY_IMAGE__", "OTP_emailheader_RegistryLogo_CA.jpg")
        #     self.fileContents = self.fileContents.replace("__NAV1_IMAGE__", "OTP_emailheader_NAV1_CA.jpg")
        #     self.fileContents = self.fileContents.replace("__NAV2_IMAGE__", "OTP_emailheader_NAV2_CA.jpg")
        #     self.fileContents = self.fileContents.replace("__NAV3_IMAGE__", "OTP_emailheader_NAV3_CA.jpg")
        # else:
        #     self.fileContents = self.fileContents.replace("__LOGO_IMAGE__", "OTP_emailheader_Logo.jpg")
        #     self.fileContents = self.fileContents.replace("__FREE_SHIPPING_IMAGE__", "OTP_emailheader_FreeShipping.jpg")
        #     self.fileContents = self.fileContents.replace("__INSTORE_IMAGE__", "OTP_emailheader_InStore.jpg")
        #     self.fileContents = self.fileContents.replace("__REGISTRY_IMAGE__", "OTP_emailheader_RegistryLogo.jpg")
        #     self.fileContents = self.fileContents.replace("__NAV1_IMAGE__", "OTP_emailheader_NAV1.jpg")
        #     self.fileContents = self.fileContents.replace("__NAV2_IMAGE__", "OTP_emailheader_NAV2.jpg")
        #     self.fileContents = self.fileContents.replace("__NAV3_IMAGE__", "OTP_emailheader_NAV3.jpg")

        return self.fileContents

    def postProcess(self, **kwargs):
        for irow in self.sheet.rows():
            if irow[self.locationColumn].strip() == 'Sub-header' and irow[self.altTextColumn].strip() != '':
                subject_line = irow[self.altTextColumn]
                break


        recipients = ["shannon.chopson@purered.net"]
        #recipients = ["110215SPR@litmustest.com", "devpurered.runme@previews.emailonacid.com", "qa@purered.net"]

        if self.sendEmail and os.path.isfile("{}/{}.html".format(self.prodPath, self.projectName)):
            mailChimp.upload(self.prodPath, self.projectName, subject_line, "dev@purered.net", "Pure Red", recipients)