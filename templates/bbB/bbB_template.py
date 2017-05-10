import pyexcel as p
from sys import argv


def readCRF(fileName):
    return p.get_book(file_name=fileName)


def findBody():
    for irow in range(0, max_rows):
        if (sheet.cell_value(irow, 0) == "Body"):
            # print "Found body at " + str(irow)
            return irow


def generateArticle(irow):
    if (sheet.cell_value(irow, 6) == "image"):
        return generateImage(irow)
    elif (sheet.cell_value(irow, 6) == "image-2-columns"):
        return generateImage2columns(irow)


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
    if (cell == "NONE"):
        return ""
    else:
        return cell


def generateImage(irow):
    contents.insert(insertRow(), "- type: 'image'" + "\n")
    contents.insert(insertRow(), "  img_link: '" + getImageLink(sheet.cell_value(irow, 4)) + "'" + "\n")
    contents.insert(insertRow(), "  img_alt: '" + encodeText(sheet.cell_value(irow, 1)) + "'" + "\n")
    contents.insert(insertRow(), "  img_url: 'images/" + getImageName(sheet.cell_value(irow, 5)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "\n")
    return 0



def generateImage2columns(irow):
    contents.insert(insertRow(), "- type: 'image-2-columns'" + "\n")
    contents.insert(insertRow(), "  img_link: '" + getImageLink(sheet.cell_value(irow, 4)) + "'" + "\n")
    contents.insert(insertRow(), "  img_alt: '" + encodeText(sheet.cell_value(irow, 1)) + "'" + "\n")
    contents.insert(insertRow(), "  img_url: 'images/" + getImageName(sheet.cell_value(irow, 5)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "  img_2_link: '" + sheet.cell_value(irow + 1, 4) + "'" + "\n")
    contents.insert(insertRow(), "  img_2_alt: '" + encodeText(sheet.cell_value(irow + 1, 1)) + "'" + "\n")
    contents.insert(insertRow(), "  img_2_url: 'images/" + getImageName(sheet.cell_value(irow + 1, 5)) + ".jpg'" + "\n")
    contents.insert(insertRow(), "\n")
    return 1


def getImageName(number):
    return imagePattern + "{:0>2d}".format(number)


# __main__
ymlFile = argv[1]
workbook = readCRF(argv[2])
imagePattern = argv[3]

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
    if (skipNextRows is not None and skipNextRows > 0):
        skipNextRows -= 1
        continue
    if (sheet.cell_value(irow, 0) == "Body" and sheet.cell_value(irow, 5) != ""):
        skipNextRows = generateArticle(irow)

outputFile = open(ymlFile, "w")
fileContents = ""
for line in contents:
    fileContents += line.encode("utf8")
outputFile.write(fileContents)
outputFile.close()