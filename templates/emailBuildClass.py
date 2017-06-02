import pyexcel as p
from sys import argv
import os
import fnmatch
import sys
import re
from shutil import copyfile
from distutils.dir_util import copy_tree

reload(sys)
sys.setdefaultencoding('utf8')


class emailBuilder(object):

    def __init__(self, crf_file, emailName):
        self.projectName = emailName
        self.erbExtension = ".html.erb"
        self.ymlExtension = ".yml"

        fullPath = os.path.abspath(os.getcwd())
        if "emails" in fullPath:
            fullPath = "emails".join(fullPath.split("emails")[:-1]) + "emails"
        else:
            raise SyntaxError("Unable to find emails repository, are you running this script from inside the emails repo?")

        self.dataPath =  fullPath + "/data/" + self.folderPath + "/" + self.projectName
        self.sourcePath = fullPath + "/source/" + self.folderPath + "/" + self.projectName
        self.imagePath = self.sourcePath + "/images"
        self.erbPath = self.sourcePath + "/" + self.projectName + self.erbExtension
        self.ymlPath = self.dataPath + "/" + self.projectName + self.ymlExtension
        self.crfFile = crf_file

        self.navBarCount = 1
        self.newLine = "\n"
        self.imageFileExtensions = ['.jpg', '.jpeg', '.gif', '.png']
        self.layoutSheetName = "Layout"
        self.fileContents = ""

    def copySourceFiles(self, source_images):
        if source_images is not None and source_images.strip() != "":
            copy_tree(source_images, self.imagePath)

    def setupTemplates(self):
        copyfile(self.ymlTemplate, self.ymlPath)
        copyfile(self.erbTemplate, self.erbPath)

        self.updateErb()

    def updateErb(self):
        erbFile = open(self.erbPath, "r")
        erbLines = erbFile.readlines()
        erbFile.close()

        erbContents = ""
        for erbLine in erbLines:
            erbContents += erbLine
        erbContents = erbContents.replace("__PROJECT_NAME__", self.projectName)
        erbFile = open(self.erbPath, "w")
        erbFile.write(erbContents)
        erbFile.close()

    def loadData(self):
        self.workbook = p.get_book(file_name=self.crfFile)

        if isinstance(self.sheetName, int) or self.sheetName.isdigit():
            self.sheet = self.workbook.sheet_by_index(self.sheetName)
        else:
            self.sheet = self.workbook.sheet_by_name(self.sheetName)

        self.layoutsheet = self.workbook.sheet_by_name(self.layoutSheetName)

        outputFile = open(self.ymlPath, "r")
        self.contents = outputFile.readlines()
        outputFile.close()

        try:
            self.templateStart = self.contents.index("#__IMAGE_TEMPLATES__\n")
        except:
            self.templateStart = 0

    def insertRow(self):
        self.templateStart += 1
        return self.templateStart

    def encodeText(self, cell):
        cell = cell.replace("&", "&amp;")
        cell = cell.replace("'", "&#39;")
        cell = cell.replace('"', "&#34;")
        cell = cell.replace('\n', "")
        return cell

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
        row = [''] * 100
        for irow in self.sheet.rows():
            if self.cellContainsImage(irow[-1], image):
                row = irow
        return row

    def getImageLink(self, cell):
        if cell == "NONE":
            return ""
        else:
            return cell

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

    def getImageRelativePathAndName(self, imageValue):
        imagePath = ""
        searchPattern = None
        regPattern = re.compile("[H,S,F]\d")
        if isinstance(imageValue, long) or imageValue.isdigit():
            searchPattern = "{:0>2d}".format(int(imageValue))
        elif regPattern.match(imageValue) is not None:
            searchPattern = imageValue

        if searchPattern is not None:
            for file in os.listdir(self.imagePath):
                for extension in self.imageFileExtensions:
                    if fnmatch.fnmatch(file, '*_' + searchPattern + extension):
                        imageValue = file

        if "http" not in imageValue:
            imagePath = "images/"

        return imagePath, imageValue

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

    def update(self):
        pass

    def createEmail(self):
        self.loadData()
        self.generateYmlContent()

        outputFile = open(self.ymlPath, "w")

        for line in self.contents:
            self.fileContents += line.encode("utf8")
        self.update()
        outputFile.write(self.fileContents)
        outputFile.close()
