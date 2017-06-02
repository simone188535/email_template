from distutils.dir_util import copy_tree
from shutil import copyfile
import pyexcel as p
from emailBuildClass import emailBuilder
from PIL import Image

class SPRBuilder(emailBuilder):
    def __init__(self, crf_file, emailName):
        self.projectNamePrefix = "SPR_"
        self.folderPath = "sprichards"
        self.ymlTemplate = "SPR/SPR_Template.yml"
        self.erbTemplateAuto = "SPR/SPR_Template_Auto.erb"
        self.erbTemplateCustom = "SPR/SPR_Template_Custom.erb"
        self.sheetName = 0
        self.altTextColumn = 2
        self.linkColumn = 14
        super(SPRBuilder, self).__init__(crf_file, emailName)
        self.customFieldCount = 1

    def setupTemplates(self):
        copyfile(self.ymlTemplate, self.ymlPath)
        self.erbAutoPath = self.erbPath.rstrip(self.erbExtension) + "_Auto" + self.erbExtension
        self.erbCustomPath = self.erbPath.rstrip(self.erbExtension) + "_Custom" + self.erbExtension
        copyfile(self.erbTemplateAuto, self.erbAutoPath)
        copyfile(self.erbTemplateCustom, self.erbCustomPath)

        self.erbPath = self.erbAutoPath
        self.updateErb()
        self.erbPath = self.erbCustomPath
        self.updateErb()


    def generateImage(self, *images):
        articleType = "table"

        self.contents.insert(self.insertRow(), "- type: '" + articleType + "'" + self.newLine)
        data = []

        for img in images:
            imgData = ['']*6
            backgroundColor = "#FFFFFF"
            textColor = "#000000"


            if ("$" in str(img)):
                imgData[0] = "image"
                img = img.lstrip("$")
                imgcolors = img.split("#")
                img = imgcolors[0]
                if len(imgcolors) > 1 and imgcolors[1].strip() != '':
                    backgroundColor = "#" + imgcolors[1]
                if len(imgcolors) > 2 and  imgcolors[2].strip() != '':
                    textColor = "#" + imgcolors[2]

                imgData[0] = "text"
                imgData.append(backgroundColor.encode('ascii','ignore'))
                imgData.append(textColor.encode('ascii','ignore'))
                imgData.append("linetext" + str(self.customFieldCount) + "_CUS")
                self.customFieldCount = self.customFieldCount + 1
            else:
                imgData[0] = "image"

            row = self.findImageRow(img)

            path, imageName = self.getImageRelativePathAndName(img)
            imgFile = Image.open(self.imagePath + "/" + imageName)
            width, height = imgFile.size

            imgData[1] = path + imageName
            imgData[2] = self.getImageLink(row[self.linkColumn]).encode('ascii','ignore')
            imgData[3] = width
            imgData[4] = height
            imgData[5] = row[self.altTextColumn].encode('ascii','ignore')

            data.append(imgData)

        self.contents.insert(self.insertRow(), "  data: " + str(data) + "" + self.newLine)
        self.contents.insert(self.insertRow(), self.newLine)