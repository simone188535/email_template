from distutils.dir_util import copy_tree
import pyexcel as p
from emailBuildClass import emailBuilder

class BLDBase(emailBuilder):
    def update(self):
        self.updateHeader()

    def updateHeader(self):
        # find and update title
        nameFound = False
        titleFound = False

        for irow in self.sheet.rows():
            for x in range(0, len(irow) - 1):
                if irow[x].strip() == "Task:":
                    self.fileContents = self.fileContents.replace("__EMAIL_NAME__", irow[x + 1])
                    nameFound = True
                elif irow[x].strip() == "Subject Line:":
                    self.fileContents = self.fileContents.replace("__TITLE__", irow[x + 1])
                    titleFound = True
                if nameFound and titleFound:
                    break
            if nameFound and titleFound:
                break

    def loadData(self):
        super(BLDBase, self).loadData()
        self.layoutSheetName = "Layout"
        self.layoutsheet = self.workbook.sheet_by_name(self.layoutSheetName)

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

class BLDNoHeaderFooter(BLDBase):
    def __init__(self, **kwargs):
        self.projectNamePrefix = "BLD_"
        self.folderPath = "balduccis"
        self.ymlTemplate = "BLD/BLD_Template_Weekly_Email_053017.yml"
        self.erbTemplate = "BLD/BLD_Template_No_Header_Footer.erb"

        self.sheetName = 0
        self.altTextColumn = 2
        self.linkColumn = 5
        super(BLDNoHeaderFooter, self).__init__(**kwargs)

class BLDWeekly(BLDBase):
    def __init__(self, **kwargs):
        self.projectNamePrefix = "BLD_"
        self.folderPath = "balduccis"
        self.ymlTemplate = "BLD/BLD_Template_Weekly_Email_053017.yml"
        self.erbTemplate = "BLD/BLD_Template_Weekly_Email_053017.erb"

        self.sheetName = 0
        self.altTextColumn = 2
        self.linkColumn = 5
        super(BLDWeekly, self).__init__(**kwargs)