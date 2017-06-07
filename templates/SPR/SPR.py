from distutils.dir_util import copy_tree
from shutil import copyfile
import pyexcel as p
from emailBuildClass import emailBuilder
from PIL import Image

hueBreakpoint = 180

class SPRBuilder(emailBuilder):
    def __init__(self, crf_file, source_images, emailName):
        self.projectNamePrefix = "SPR_"
        self.folderPath = "sprichards"
        self.ymlTemplate = "SPR/SPR_Template.yml"
        self.erbTemplateAuto = "SPR/SPR_Template_Auto.erb"
        self.erbTemplateCustom = "SPR/SPR_Template_Custom.erb"
        self.sheetName = 0
        self.altTextColumn = 2
        self.linkColumn = 18
        super(SPRBuilder, self).__init__(crf_file, source_images, emailName)
        self.customFieldCount = 1
        self.pageWidth = 0

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

    def isImageCustomField(self, img):
        customField = False

        if "Custom" in self.workbook.sheet_names():
            customSheet = self.workbook.sheet_by_name("Custom")
            for row in customSheet.rows():
                if self.cellContainsImage(irow[-1], img):
                    customField = True

        return customField

    def addAdditionalFields(self, img, imgData):

        textColor = ""
        backgroundColor = ""

        if (self.isImageCustomField(img)):
            imgData[0] = "text"
            imgFile = imgFile.convert('RGB')
            colors = imgFile.getcolors(100000000)
            colorSingle = imgFile.getpixel((0, 0))
            if len(colors) > 0:
                count, backgroundColor = colors[0]
                if count < 250:
                    backgroundColor = colorSingle
                hue = backgroundColor[0] * 0.299 + backgroundColor[1] * 0.587 + backgroundColor[2] * 0.114
                if (hue) > hueBreakpoint:
                    textColor = "#000000"
                else:
                    textColor = "#FFFFFF"
                backgroundColor = '#%02x%02x%02x' % backgroundColor

            imgData.append(backgroundColor.encode('ascii', 'ignore'))
            imgData.append(textColor.encode('ascii', 'ignore'))
            imgData.append("linetext" + str(self.customFieldCount) + "_CUS")
            self.customFieldCount = self.customFieldCount + 1
        else:
            imgData[0] = "image"

        return imgData