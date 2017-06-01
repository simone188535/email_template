from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuilder import encodeText

class bbB(object):
    def __init__(self):
        self.projectNamePrefix = "bbB_"
        self.folderPath = "buybuyBaby"
        self.ymlTemplate = "bbB/bbB_Template_05012017.yml"
        self.erbTemplate = "bbB/bbB_Template_05012017.erb"

    def setup(self, crf_file, imagePath):
        copy_tree("bbB/social_images", imagePath)

        if "CANADA" in crf_file.upper():
            copy_tree("bbB/CA_images", imagePath)
            self.sheet = "ASF"
            self.altTextColumn = 2
            self.linkColumn = 5
            self.locationColumn = 1
            self.canada = True
        else:
            copy_tree("bbB/US_images", imagePath)
            self.sheet = "Link Table"
            self.altTextColumn = 1
            self.linkColumn = 4
            self.locationColumn = 0
            self.canada = False

    def update(self, fileContents, sheet):
        fileContents = self.updateHeader(fileContents, sheet)
        return fileContents

    def updateNavBar(self, row, navBarCount, fileContents):
        fileContents = fileContents.replace("__NAV" + str(navBarCount) + "_ALT__", encodeText(row[self.altTextColumn]))
        fileContents = fileContents.replace("__NAV" + str(navBarCount) + "_LINK__", encodeText(row[self.linkColumn]))
        navBarCount += 1

        return navBarCount, fileContents

    def updateSubHeader(self, row, fileContents):
        altText = row[self.altTextColumn]
        if altText == "View as a web page":
            fileContents = fileContents.replace("__WEBPAGE_LINK__", row[self.linkColumn])
        elif altText == "buybuy Baby Logo" or row[self.altTextColumn] == "buybuy Canada Baby Logo":
            fileContents = fileContents.replace("__LOGO_LINK__", row[self.linkColumn])
            fileContents = fileContents.replace("__LOGO_ALT__", encodeText(row[self.altTextColumn]))
        elif "FREE SHIPPING ON ORDERS OVER $49" in altText.upper():
            fileContents = fileContents.replace("__FREE_SHIPPING_LINK__", row[self.linkColumn])
        elif "IN-STORE PICKUP" in altText.upper():
            fileContents = fileContents.replace("__INSTORE_LINK__", row[self.linkColumn])
        elif altText == "baby registry logo":
            fileContents = fileContents.replace("__REGISTRY_LINK__", row[self.linkColumn])

        return fileContents

    def updateHeader(self, fileContents, sheet):
        # find and update title
        for irow in sheet.rows():
            if irow[self.locationColumn] == "Sub-header":
                fileContents = fileContents.replace("__EMAIL_TITLE__", encodeText(irow[self.altTextColumn]))
                fileContents = fileContents.replace("__EMAIL_TITLE_LINK__", irow[self.linkColumn])
                break

        navBarCount = 1

        for irow2 in sheet.rows():
            if irow2[self.locationColumn] == "Sub-header":
                fileContents = self.updateSubHeader(irow2, fileContents)
            elif irow2[self.locationColumn] == "Header Bar":
                navBarCount, fileContents = self.updateNavBar(irow2, navBarCount, fileContents)

        if (self.canada):
            fileContents = fileContents.replace("__LOGO_IMAGE__", "bbB_emailheader_Logo_CA.jpg")
            fileContents = fileContents.replace("__FREE_SHIPPING_IMAGE__", "bbB_emailheader_FreeShipping_CA.jpg")
            fileContents = fileContents.replace("__INSTORE_IMAGE__", "bbB_emailheader_InStore_CA.jpg")
            fileContents = fileContents.replace("__REGISTRY_IMAGE__", "bbB_emailheader_RegistryLogo_CA.jpg")
            fileContents = fileContents.replace("__NAV1_IMAGE__", "bbB_emailheader_NAV1_CA.jpg")
            fileContents = fileContents.replace("__NAV2_IMAGE__", "bbB_emailheader_NAV2_CA.jpg")
            fileContents = fileContents.replace("__NAV3_IMAGE__", "bbB_emailheader_NAV3_CA.jpg")
        else:
            fileContents = fileContents.replace("__LOGO_IMAGE__", "bbB_emailheader_Logo.jpg")
            fileContents = fileContents.replace("__FREE_SHIPPING_IMAGE__", "bbB_emailheader_FreeShipping.jpg")
            fileContents = fileContents.replace("__INSTORE_IMAGE__", "bbB_emailheader_InStore.jpg")
            fileContents = fileContents.replace("__REGISTRY_IMAGE__", "bbB_emailheader_RegistryLogo.jpg")
            fileContents = fileContents.replace("__NAV1_IMAGE__", "bbB_emailheader_NAV1.jpg")
            fileContents = fileContents.replace("__NAV2_IMAGE__", "bbB_emailheader_NAV2.jpg")
            fileContents = fileContents.replace("__NAV3_IMAGE__", "bbB_emailheader_NAV3.jpg")

        return fileContents