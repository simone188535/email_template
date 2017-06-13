from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuildClass import emailBuilder

class KFLoyalty(emailBuilder):
    def __init__(self, **kwargs):
        self.projectNamePrefix = "KF_"
        self.folderPath = "kingsfoodmarkets"
        self.ymlTemplate = "KF/KF_Template_Loyalty_Email_053117.yml"
        self.erbTemplate = "KF/KF_Template_Loyalty_Email_053117.erb"

        self.sheetName = 0
        self.altTextColumn = 2
        self.linkColumn = 5
        super(KFLoyalty, self).__init__(**kwargs)

    def update(self):
        self.updateHeader()

    def updateHeader(self):
        # find and update title
        nameFound = False
        titleFound = False

        for irow in self.sheet.rows():
            for x in range(0, len(irow) -1):
                if irow[x].strip() == "Task:":
                    self.fileContents = self.fileContents.replace("__EMAIL_NAME__", irow[x+1])
                    nameFound = True
                elif irow[x].strip() == "Subject:":
                    self.fileContents = self.fileContents.replace("__TITLE__", irow[x+1])
                    titleFound = True
                if nameFound and titleFound:
                    break
            if nameFound and titleFound:
                break

    def loadData(self):
        super(KFLoyalty, self).loadData()
        self.layoutSheetName = "Layout"
        self.layoutsheet = self.workbook.sheet_by_name(self.layoutSheetName)

    def generateImage(self, *images):
        if len(images) == 5:
            type = "image-5-columns"
        elif len(images) == 4:
            type = "image-4-columns"
        elif len(images) == 3:
            type = "image-3-columns"
        elif len(images) == 2:
            type = "image-2-columns"
        else:
            type = "image"

        self.contents.insert(self.insertRow(), "- type: '" + type + "'" + self.newLine)

        row1 = self.findImageRow(images[0])
        path, imageName = self.getImageRelativePathAndName(images[0])
        self.contents.insert(self.insertRow(), "  img_link: '" + self.getImageLink(row1[self.linkColumn]) + "'" + self.newLine)
        self.contents.insert(self.insertRow(), "  img_alt: '" + self.encodeText(row1[self.altTextColumn]) + "'" + self.newLine)
        self.contents.insert(self.insertRow(), "  img_url: '" + path + imageName + "'" + self.newLine)

        if len(images) > 1:
            row2 = self.findImageRow(images[1])
            path, imageName = self.getImageRelativePathAndName(images[1])
            self.contents.insert(self.insertRow(), "  img_2_link: '" + self.getImageLink(row2[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_2_alt: '" + self.encodeText(row2[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_2_url: '" + path + imageName + "'" + self.newLine)

        if len(images) > 2:
            row3 = self.findImageRow(images[2])
            path, imageName = self.getImageRelativePathAndName(images[2])
            self.contents.insert(self.insertRow(), "  img_3_link: '" + self.getImageLink(row3[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_3_alt: '" + self.encodeText(row3[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_3_url: '" + path + imageName + "'" + self.newLine)

        if len(images) > 3:
            row4 = self.findImageRow(images[3])
            path, imageName = self.getImageRelativePathAndName(images[3])
            self.contents.insert(self.insertRow(), "  img_4_link: '" + self.getImageLink(row4[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_4_alt: '" + self.encodeText(row4[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_4_url: '" + path + imageName + "'" + self.newLine)

        if len(images) > 4:
            row5 = self.findImageRow(images[4])
            path, imageName = self.getImageRelativePathAndName(images[4])
            self.contents.insert(self.insertRow(), "  img_5_link: '" + self.getImageLink(row5[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_5_alt: '" + self.encodeText(row5[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_5_url: '" + path + imageName + "'" + self.newLine)

        self.contents.insert(self.insertRow(), self.newLine)

    def generateYmlContent(self):
        for irow in self.layoutsheet.rows():
            while '' in irow:
                irow.remove('')

            if len(irow) == 1:
                self.generateImage(irow[0])
            elif len(irow) == 2:
                self.generateImage(irow[0], irow[1])
            elif len(irow) == 3:
                self.generateImage(irow[0], irow[1], irow[2])
            elif len(irow) == 4:
                self.generateImage(irow[0], irow[1], irow[2], irow[3])
            elif len(irow) == 5:
                self.generateImage(irow[0], irow[1], irow[2], irow[3], irow[4])