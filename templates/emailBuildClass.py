import pyexcel as p
from sys import argv
import os
import fnmatch
import sys
import re
from shutil import copyfile
from distutils.dir_util import copy_tree
from PIL import Image
from natsort import natsorted

reload(sys)
sys.setdefaultencoding('utf8')


class emailBuilder(object):

    def __init__(self, **kwargs):
        if "crf_file" in kwargs:
            self.crf_file = kwargs["crf_file"]
        if "source_images" in kwargs:
            self.source_images = kwargs["source_images"]
        if "emailName" in kwargs:
            self.projectName = kwargs["emailName"]

        self.erbExtension = ".html.erb"
        self.ymlExtension = ".yml"

        fullPath = os.path.abspath(os.getcwd())
        if "emails" in fullPath:
            fullPath = "emails".join(fullPath.split("emails")[:-1]) + "emails"
        else:
            raise SyntaxError("Unable to find emails repository, are you running this script from inside the emails repo?")

        self.dataPath =  fullPath + "/data/" + self.folderPath + "/" + self.projectName
        self.sourcePath = fullPath + "/source/" + self.folderPath + "/" + self.projectName
        self.prodPath = fullPath + "/prod/" + self.folderPath + "/" + self.projectName
        self.imagePath = self.sourcePath + "/images"
        self.erbPath = self.sourcePath + "/" + self.projectName + self.erbExtension
        self.ymlPath = self.dataPath + "/" + self.projectName + self.ymlExtension

        self.maxWidth = 600
        self.newLine = "\n"
        self.imageFileExtensions = ['jpg', 'jpeg', 'gif', 'png']
        self.fileContents = ""
        self.imageList = []

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
        self.workbook = p.get_book(file_name=self.crf_file)

        if isinstance(self.sheetName, int) or self.sheetName.isdigit():
            self.sheet = self.workbook.sheet_by_index(self.sheetName)
        else:
            self.sheet = self.workbook.sheet_by_name(self.sheetName)

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
        cell = cell.replace(u"\u2122", '&#8482;')
        cell = cell.replace(u"\u00ae", '&#174;')
        cell = cell.replace(u"\u00a9", '&#169;')
        return cell

    def cellContainsImage(self, data, image):
        data = str(data)
        match = False
        if data == image:
            match =  True
        elif '-' in data:
            data = self.convertToRange(data)

        if not match and ',' in data:
            dataList = data.split(',')
            for item in dataList:
                item = item.strip()
                if item == image:
                    match = True
                    break
                elif item.isdigit():
                    for extension in self.imageFileExtensions:
                        regPattern = re.compile(".*_{}\.{}".format("{:0>2d}".format(int(item)), extension))
                        if regPattern.match(image) is not None:
                            match = True
                            break
        elif not match and data.isdigit():
            for extension in self.imageFileExtensions:
                regPattern = re.compile(".*_{}\.{}".format("{:0>2d}".format(int(data)), extension))
                if regPattern.match(image) is not None:
                    match = True
                    break
        return match

    def convertToRange(self, data):
        newData = []
        dataList = str(data).split(',')
        for item in dataList:
            regPattern = re.compile("\d+-\d+")
            if regPattern.match(item) is not None:
                min, max = item.split('-')
                for i in range(int(min),int(max)+1):
                    newData.append(str(i))
            else:
                newData.append(str(item))
        data = ','.join(newData)
        return data


    def findImageRow(self, image):

        row = [''] * 100
        for irow in self.sheet.rows():
            if self.cellContainsImage(irow[-1], image):
                row = irow
                break
        return row

    def getImageLink(self, cell):
        if cell == "NONE":
            return ""
        else:
            return str(cell).encode('ascii',errors='ignore').strip()

    def addAdditionalFields(self, image, imgData):
        return imgData

    def generateImageTables(self):
        articleType = "table"

        tableWidth = 0
        tables = []
        thisTable = []

        for image in self.imageList:
            print('the image is' + image)
            imgData = ['']*6

            imgFile = Image.open(self.imagePath + "/" + image)

            row = self.findImageRow(image)

            width, height = imgFile.size
            imgData[0] = "image"
            imgData[1] = "images/" + image
            imgData[2] = self.getImageLink(row[self.linkColumn]).encode('ascii','ignore')
            imgData[3] = width
            imgData[4] = height
            imgData[5] = self.encodeText(row[self.altTextColumn]).encode('ascii', 'ignore')

            #imgFile.close()
            imgData = self.addAdditionalFields(image, imgData)

            tableWidth = tableWidth + width

            if tableWidth <= self.maxWidth:
                thisTable.append(imgData)

            if tableWidth > self.maxWidth:
                tables.append(thisTable)
                thisTable = []
                thisTable.append(imgData)
                tableWidth = width

        if len(thisTable) > 0:
            tables.append(thisTable)
            thisTable = []

        for table in tables:
            self.contents.insert(self.insertRow(), "- type: '" + articleType + "'" + self.newLine)
            self.contents.insert(self.insertRow(), "  data: " + str(table) + "" + self.newLine)
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

    def try_int(s):
        "Convert to integer if possible."
        try:
            return int(s)
        except:
            return s

    def generateYmlContent(self):
        for file in os.listdir(self.source_images):
            for extension in self.imageFileExtensions:
                regPattern = re.compile(".*\d+\." + extension)
                if regPattern.match(file) is not None:
                    self.imageList.append(file)


        self.imageList = natsorted(self.imageList)

        self.generateImageTables()

    def update(self):
        pass

    def postProcess(self, **kwargs):
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
