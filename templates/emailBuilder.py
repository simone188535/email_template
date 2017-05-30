import pyexcel as p
from sys import argv
import os
import fnmatch
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


def encodeText(cell):
    cell = cell.replace("&", "&amp;")
    cell = cell.replace("'", "&#39;")
    cell = cell.replace('"', "&#34;")
    cell = cell.replace('\n', "")
    return cell

class emailBuilder(object):

    def __init__(self, ymlFile, crfFile, images, sheetNameInput, altTextColumnInput, linkColumnInput):
        self.navBarCount = 1
        self.newLine = "\n"
        self.imageFileExtensions = ['.jpg', '.jpeg', '.gif', '.png']
        self.layoutSheetName = "Layout"
        self.filecontents = ""
        self.ymlFile = ymlFile

        self.imageDir = images
        self.workbook = p.get_book(file_name=crfFile)

        if isinstance(sheetNameInput, int) or sheetNameInput.isdigit():
            self.sheet = self.workbook.sheet_by_index(sheetNameInput)
        else:
            self.sheet = self.workbook.sheet_by_name(sheetNameInput)
        self.altTextColumn = altTextColumnInput
        self.linkColumn = linkColumnInput

        self.layoutsheet = self.workbook.sheet_by_name(self.layoutSheetName)

        outputFile = open(ymlFile, "r")
        self.contents = outputFile.readlines()
        outputFile.close()

        try:
            self.templateStart = self.contents.index("#__IMAGE_TEMPLATES__\n")
        except:
            self.templateStart = 0

    def insertRow(self):
        self.templateStart += 1
        return self.templateStart

    def cellContainsImage(self, data, image):
        match = False
        if data == image:
            match =  True
        elif ',' in str(data):
            dataList = str(data).split(',')
            for item in dataList:
                if item == str(image):
                    match = True
        return match

    def findImageRow(self, image):
        for irow in self.sheet.rows():
            if self.cellContainsImage(irow[-1], image):
                return irow

    def getImageLink(self, cell):
        if cell == "NONE":
            return ""
        else:
            return cell

    def generateImage(self, image1, image2=None, image3=None, image4=None, image5=None):
        if image5 is not None:
            type = "image-5-columns"
        elif image4 is not None:
            type = "image-4-columns"
        elif image3 is not None:
            type = "image-3-columns"
        elif image2 is not None:
            type = "image-2-columns"
        else:
            type = "image"

        self.contents.insert(self.insertRow(), "- type: '" + type + "'" + self.newLine)

        row1 = self.findImageRow(image1)
        self.contents.insert(self.insertRow(), "  img_link: '" + self.getImageLink(row1[self.linkColumn]) + "'" + self.newLine)
        self.contents.insert(self.insertRow(), "  img_alt: '" + encodeText(row1[self.altTextColumn]) + "'" + self.newLine)
        self.contents.insert(self.insertRow(), "  img_url: '" + self.getImageName(image1) + "'" + self.newLine)

        if image2 is not None:
            row2 = self.findImageRow(image2)
            self.contents.insert(self.insertRow(), "  img_2_link: '" + self.getImageLink(row2[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_2_alt: '" + encodeText(row2[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_2_url: '" + self.getImageName(image2) + "'" + self.newLine)

        if image3 is not None:
            row3 = self.findImageRow(image3)
            self.contents.insert(self.insertRow(), "  img_3_link: '" + self.getImageLink(row3[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_3_alt: '" + encodeText(row3[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_3_url: '" + self.getImageName(image3) + "'" + self.newLine)

        if image4 is not None:
            row4 = self.findImageRow(image4)
            self.contents.insert(self.insertRow(), "  img_4_link: '" + self.getImageLink(row4[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_4_alt: '" + encodeText(row4[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_4_url: '" + self.getImageName(image4) + "'" + self.newLine)

        if image5 is not None:
            row5 = self.findImageRow(image5)
            self.contents.insert(self.insertRow(), "  img_5_link: '" + self.getImageLink(row5[self.linkColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_5_alt: '" + encodeText(row5[self.altTextColumn]) + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  img_5_url: '" + self.getImageName(image5) + "'" + self.newLine)

        self.contents.insert(self.insertRow(), self.newLine)


    def getImageName(self, imageValue):
        searchPattern = None
        regPattern = re.compile("[H,S,F]\d")
        if isinstance(imageValue, long) or imageValue.isdigit():
            searchPattern = "{:0>2d}".format(imageValue)
        elif regPattern.match(imageValue) is not None:
            searchPattern = imageValue

        if searchPattern is not None:
            for file in os.listdir(self.imageDir):
                for extension in self.imageFileExtensions:
                    if fnmatch.fnmatch(file, '*_' + searchPattern + extension):
                        imageValue = file

        if "http" not in imageValue:
            imageValue = "images/" + imageValue

        return imageValue

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

    def createEmail(self, emailData):
        self.generateYmlContent()

        outputFile = open(self.ymlFile, "w")

        for line in self.contents:
            self.filecontents += line.encode("utf8")
        self.filecontents = emailData.update(self.filecontents, self.sheet)
        outputFile.write(self.filecontents)
        outputFile.close()
