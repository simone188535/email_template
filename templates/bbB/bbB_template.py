import pyexcel as p
from sys import argv

navBarCount = 1

ymlFile = argv[1]
workbook = p.get_book(file_name=argv[2])
imagePattern = argv[3]

if "CRF" in argv[2] and workbook.sheet_by_name("Link Table") is not None:
    locationColumn = 0
    altTextColumn = 1
    linkColumn = 4
    imageColumn = 5
    imageTypeColumn = 6
elif "ASF" in argv[2] and workbook.sheet_by_name("ASF") is not None:
    locationColumn = 1
    altTextColumn = 2
    linkColumn = 5
    imageColumn = 6
    imageTypeColumn = 7

if "CANADA" in argv[2].upper():
    canada = True

#__methods__
def updateNavBar(row):
    global navBarCount
    global fileContents

    fileContents = fileContents.replace("__NAV" + str(navBarCount) + "_ALT__", encodeText(sheet.cell_value(row, altTextColumn)))
    fileContents = fileContents.replace("__NAV" + str(navBarCount) + "_LINK__", encodeText(sheet.cell_value(row, linkColumn)))
    navBarCount += 1


def updateSubHeader(row):
    global fileContents

    altText = sheet.cell_value(row, altTextColumn)
    if altText == "View as a web page":
        fileContents = fileContents.replace("__WEBPAGE_LINK__", sheet.cell_value(row, linkColumn))
    elif altText == "buybuy Baby Logo" or sheet.cell_value(row, altTextColumn) == "buybuy Canada Baby Logo":
        fileContents = fileContents.replace("__LOGO_LINK__", sheet.cell_value(row, linkColumn))
        fileContents = fileContents.replace("__LOGO_ALT__", encodeText(sheet.cell_value(row, altTextColumn)))
    elif "FREE SHIPPING ON ORDERS OVER $49" in altText.upper():
        fileContents = fileContents.replace("__FREE_SHIPPING_LINK__", sheet.cell_value(row, linkColumn))
    elif "IN-STORE PICKUP" in altText.upper():
        fileContents = fileContents.replace("__INSTORE_LINK__", sheet.cell_value(row, linkColumn))
    elif altText == "baby registry logo":
        fileContents = fileContents.replace("__REGISTRY_LINK__", sheet.cell_value(row, linkColumn))


def updateHeaderAndFooter():
    global fileContents
    for irow1 in range(0, max_rows):
        if sheet.cell_value(irow1, locationColumn) == "Sub-header":
            fileContents = fileContents.replace("__EMAIL_TITLE__", encodeText(sheet.cell_value(irow1, altTextColumn)))
            fileContents = fileContents.replace("__EMAIL_TITLE_LINK__", sheet.cell_value(irow1, linkColumn))
            break

    for irow2 in range(0, max_rows):
        if sheet.cell_value(irow2, locationColumn) == "Sub-header":
            updateSubHeader(irow2)
        elif sheet.cell_value(irow2, locationColumn) == "Header Bar":
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

def findBody():
    for irow1 in range(0, max_rows):
        if sheet.cell_value(irow1, locationColumn) == "Body":
            return irow1


def generateArticle(row):
    if sheet.cell_value(row, imageTypeColumn) == "image":
        return generateImage(row)
    elif sheet.cell_value(row, imageTypeColumn) == "image-2-columns":
        return generateImage2columns(row)
    elif sheet.cell_value(row, imageTypeColumn) == "image-3-columns":
        return generateImage3columns(row)


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


def generateImage(row):
    contents.insert(insertRow(), "- type: 'image'" + "\n")
    contents.insert(insertRow(), "  img_link: '" + getImageLink(sheet.cell_value(row, linkColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_alt: '" + encodeText(sheet.cell_value(row, altTextColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_url: 'images/" + getImageName(sheet.cell_value(row, imageColumn)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "\n")
    return 0



def generateImage2columns(row):
    contents.insert(insertRow(), "- type: 'image-2-columns'" + "\n")
    contents.insert(insertRow(), "  img_link: '" + getImageLink(sheet.cell_value(row, linkColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_alt: '" + encodeText(sheet.cell_value(row, altTextColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_url: 'images/" + getImageName(sheet.cell_value(row, imageColumn)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "  img_2_link: '" + sheet.cell_value(row + 1, linkColumn) + "'" + "\n")
    contents.insert(insertRow(), "  img_2_alt: '" + encodeText(sheet.cell_value(row + 1, altTextColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_2_url: 'images/" + getImageName(sheet.cell_value(row + 1, imageColumn)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "\n")
    return 1

def generateImage3columns(row):
    contents.insert(insertRow(), "- type: 'image-3-columns'" + "\n")
    contents.insert(insertRow(), "  img_link: '" + getImageLink(sheet.cell_value(row, linkColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_alt: '" + encodeText(sheet.cell_value(row, altTextColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_url: 'images/" + getImageName(sheet.cell_value(row, imageColumn)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "  img_2_link: '" + sheet.cell_value(row + 1, linkColumn) + "'" + "\n")
    contents.insert(insertRow(), "  img_2_alt: '" + encodeText(sheet.cell_value(row + 1, altTextColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_2_url: 'images/" + getImageName(sheet.cell_value(row + 1, imageColumn)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "  img_3_link: '" + sheet.cell_value(row + 2, linkColumn) + "'" + "\n")
    contents.insert(insertRow(), "  img_3_alt: '" + encodeText(sheet.cell_value(row + 2, altTextColumn)) + "'" + "\n")
    contents.insert(insertRow(), "  img_3_url: 'images/" + getImageName(sheet.cell_value(row + 2, imageColumn)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "\n")
    return 2


def getImageName(number):
    return imagePattern + "{:0>2d}".format(number)


# __main__
if canada:
    sheet = workbook.sheet_by_name("ASF")
else:
    sheet = workbook.sheet_by_name("Link Table")

max_rows = sheet.number_of_rows()

outputFile = open(ymlFile, "r")
contents = outputFile.readlines()
outputFile.close()


try:
    templateStart = contents.index("#__IMAGE_TEMPLATES\n")
except:
    templateStart = 0

skipNextRows = 0

for irow in range(findBody(), max_rows):
    if skipNextRows is not None and skipNextRows > 0:
        skipNextRows -= 1
        continue
    if sheet.cell_value(irow, locationColumn) == "Body" and sheet.cell_value(irow, imageColumn) != "":
        skipNextRows = generateArticle(irow)

outputFile = open(ymlFile, "w")
fileContents = ""
for line in contents:
    fileContents += line.encode("utf8")
updateHeaderAndFooter()
outputFile.write(fileContents)
outputFile.close()