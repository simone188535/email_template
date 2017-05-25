import pyexcel as p
from sys import argv
import os
import fnmatch
import sys

navBarCount = 1
reload(sys)
sys.setdefaultencoding('utf8')

#Configurable options
newLine = "\n"
imageFileExtensions = ['.jpg','.jpeg','.gif','.png']

ymlFile = argv[1]
workbook = p.get_book(file_name=argv[2])
imagePattern = argv[3]
layoutSheetName = "Layout"

if "CRF" in argv[2] and workbook.sheet_by_name("Link Table") is not None:
    locationColumn = 0
    altTextColumn = 1
    linkColumn = 4
    imageColumn = 5
elif "ASF" in argv[2] and workbook.sheet_by_name("ASF") is not None:
    locationColumn = 1
    altTextColumn = 2
    linkColumn = 5
    imageColumn = 6

if "CANADA" in argv[2].upper():
    canada = True
else:
    canada = False

#__methods__
def updateNavBar(row):
    global navBarCount
    global fileContents

    fileContents = fileContents.replace("__NAV" + str(navBarCount) + "_ALT__", encodeText(row[altTextColumn]))
    fileContents = fileContents.replace("__NAV" + str(navBarCount) + "_LINK__", encodeText(row[linkColumn]))
    navBarCount += 1


def updateSubHeader(row):
    global fileContents

    altText = row[altTextColumn]
    if altText == "View as a web page":
        fileContents = fileContents.replace("__WEBPAGE_LINK__", row[linkColumn])
    elif altText == "buybuy Baby Logo" or row[altTextColumn] == "buybuy Canada Baby Logo":
        fileContents = fileContents.replace("__LOGO_LINK__", row[linkColumn])
        fileContents = fileContents.replace("__LOGO_ALT__", encodeText(row[altTextColumn]))
    elif "FREE SHIPPING ON ORDERS OVER $49" in altText.upper():
        fileContents = fileContents.replace("__FREE_SHIPPING_LINK__", row[linkColumn])
    elif "IN-STORE PICKUP" in altText.upper():
        fileContents = fileContents.replace("__INSTORE_LINK__", row[linkColumn])
    elif altText == "baby registry logo":
        fileContents = fileContents.replace("__REGISTRY_LINK__", row[linkColumn])


def updateHeaderAndFooter():
    global fileContents
    #find and update title
    for irow in sheet.rows():
        if irow[locationColumn] == "Sub-header":
            fileContents = fileContents.replace("__EMAIL_TITLE__", encodeText(irow[altTextColumn]))
            fileContents = fileContents.replace("__EMAIL_TITLE_LINK__", irow[linkColumn])
            break

    for irow2 in sheet.rows():
        if irow2[locationColumn] == "Sub-header":
            updateSubHeader(irow2)
        elif irow2[locationColumn] == "Header Bar":
            updateNavBar(irow2)

    if (canada):
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

def cellContainsImage(data, image):
    match = False
    if data == image:
        match =  True
    elif ',' in str(data):
        dataList = str(data).split(',')
        for item in dataList:
            if item == str(image):
                match = True
    return match

def findImageRow(image):
    for irow in sheet.rows():
        if cellContainsImage(irow[imageColumn], image):
            return irow


def insertRow():
    global templateStart
    templateStart += 1
    return templateStart


def encodeText(cell):
    cell = cell.replace("&", "&amp;")
    cell = cell.replace("'", "&#39;")
    cell = cell.replace('"', "&#34;")
    return cell

def getImageLink(cell):
    if cell == "NONE":
        return ""
    else:
        return cell

def generateImage(image1, image2=None, image3=None, image4=None, image5=None):
    if image3 is not None:
        type = "image-3-columns"
    elif image2 is not None:
        type = "image-2-columns"
    else:
        type = "image"

    contents.insert(insertRow(), "- type: '" + type + "'" + newLine)

    row = findImageRow(image1)
    contents.insert(insertRow(), "  img_link: '" + getImageLink(row[linkColumn]) + "'" + newLine)
    contents.insert(insertRow(), "  img_alt: '" + encodeText(row[altTextColumn]) + "'" + newLine)
    contents.insert(insertRow(), "  img_url: 'images/" + getImageName(image1) + "'" + newLine)

    if image2 is not None:
        row2 = findImageRow(image2)
        contents.insert(insertRow(), "  img_2_link: '" + getImageLink(row2[linkColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_2_alt: '" + encodeText(row2[altTextColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_2_url: 'images/" + getImageName(image2) + "'" + newLine)

    if image3 is not None:
        row3 = findImageRow(image3)
        contents.insert(insertRow(), "  img_3_link: '" + getImageLink(row3[linkColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_3_alt: '" + encodeText(row3[altTextColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_3_url: 'images/" + getImageName(image3) + "'" + newLine)

    if image4 is not None:
        row4 = findImageRow(image4)
        contents.insert(insertRow(), "  img_3_link: '" + getImageLink(row4[linkColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_3_alt: '" + encodeText(row4[altTextColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_3_url: 'images/" + getImageName(image4) + "'" + newLine)

    if image4 is not None:
        row5 = findImageRow(image5)
        contents.insert(insertRow(), "  img_3_link: '" + getImageLink(row5[linkColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_3_alt: '" + encodeText(row5[altTextColumn]) + "'" + newLine)
        contents.insert(insertRow(), "  img_3_url: 'images/" + getImageName(image5) + "'" + newLine)

    contents.insert(insertRow(), newLine)


def getImageName(imageValue):
    if isinstance(imageValue, long) or imageValue.isdigit():
        for file in os.listdir(imagePattern):
            for extension in imageFileExtensions:
                if fnmatch.fnmatch(file, '*_' + "{:0>2d}".format(imageValue) + extension):
                    return file
    else:
        return imageValue

def generateYmlContent():
    for irow in layoutSheet.rows():
        while '' in irow:
            irow.remove('')

        if len(irow) == 1:
            generateImage(irow[0])
        elif len(irow) == 2:
            generateImage(irow[0], irow[1])
        elif len(irow) == 3:
            generateImage(irow[0], irow[1], irow[2])
        elif len(irow) == 4:
            generateImage(irow[0], irow[1], irow[2], irow[3])
        elif len(irow) == 5:
            generateImage(irow[0], irow[1], irow[2], irow[3], irow[4])

# __main__
if canada:
    sheet = workbook.sheet_by_name("ASF")
else:
    sheet = workbook.sheet_by_name("Link Table")

layoutSheet = workbook.sheet_by_name(layoutSheetName)

outputFile = open(ymlFile, "r")
contents = outputFile.readlines()
outputFile.close()

try:
    templateStart = contents.index("#__IMAGE_TEMPLATES\n")
except:
    templateStart = 0

generateYmlContent()


outputFile = open(ymlFile, "w")
fileContents = ""
for line in contents:
    fileContents += line.encode("utf8")
updateHeaderAndFooter()
outputFile.write(fileContents)
outputFile.close()
