from distutils.dir_util import copy_tree
from shutil import copyfile
import pyexcel as p
from emailBuildClass import emailBuilder
from PIL import Image

hueBreakpoint = 180

class SPRBuilder(emailBuilder):
    def __init__(self, **kwargs):
        self.projectNamePrefix = "SPR_"
        self.folderPath = "sprichards"
        self.ymlTemplate = "SPR/SPR_Template.yml"
        self.erbTemplateAuto = "SPR/SPR_Template_Auto.erb"
        self.erbTemplateCustom = "SPR/SPR_Template_Custom.erb"
        self.sheetName = 0
        self.altTextColumn = "Full Sku"
        self.linkColumn = "CONCATENATE"
        super(SPRBuilder, self).__init__(**kwargs)
        self.customFieldCount = 1
        self.customSheet = None
        self.maxWidth = 580

    def loadData(self):
        super(SPRBuilder, self).loadData()
        headerrow = self.sheet.row[0]
        foundAltText = False
        foundLink = False
        for row in headerrow:
            if not foundAltText and row.strip().upper() == self.altTextColumn.upper():
                self.altTextColumn = headerrow.index(row)
                foundAltText = True
            elif not foundLink and row.strip().upper() == self.linkColumn.upper():
                self.linkColumn = headerrow.index(row)
                foundLink = True

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

        if self.customSheet is None and "Custom" in self.workbook.sheet_names():
            self.customSheet = self.workbook.sheet_by_name("Custom")

        if self.customSheet is not None:
            for row in self.customSheet.rows():
                for value in row:
                    if self.cellContainsImage(value, img):
                        customField = True

        return customField

    def getImageColors(self, image):
        backgroundColor = ""
        textColor = ""

        imgFile = Image.open(self.imagePath + "/" + image)
        imgFile = imgFile.convert('RGB')
        colors = imgFile.getcolors(100000000)
        colorSingle = imgFile.getpixel((0, 0))
        if len(colors) > 0:
            count, backgroundColor = colors[0]
            if count < 250 or colorSingle not in colors:
                backgroundColor = colorSingle
            hue = backgroundColor[0] * 0.299 + backgroundColor[1] * 0.587 + backgroundColor[2] * 0.114
            if (hue) > hueBreakpoint:
                textColor = "#000000"
            else:
                textColor = "#FFFFFF"
            backgroundColor = '#%02x%02x%02x' % backgroundColor

        return backgroundColor, textColor

    def addCustomFieldData(self, image, imgData):
        backgroundColor, textColor = self.getImageColors(image)

        imgData.append(backgroundColor.encode('ascii', 'ignore'))
        imgData.append(textColor.encode('ascii', 'ignore'))
        imgData.append("linetext" + str(self.customFieldCount) + "_CUS")
        self.customFieldCount = self.customFieldCount + 1


    def addAdditionalFields(self, image, imgData):
        if (self.isImageCustomField(image)):
            imgData[0] = "text"
            self.addCustomFieldData(image, imgData)
        elif image == self.imageList[-1]:
            imgData[0] = "footer"
            self.addCustomFieldData(image, imgData)

        return imgData