from emailBuildClass import emailBuilder

class genericEmailBuilder(emailBuilder):
    def __init__(self, crf_file, source_images, emailName):
        self.projectNamePrefix = "email_"
        self.folderPath = "other"
        self.ymlTemplate = "generic_Template_053017.yml"
        self.erbTemplate = "generic_Template_053017.erb"

        self.sheet = raw_input("Enter Excel Sheet Name with Email Data\n")
        self.altTextColumn = raw_input("Enter Excel Column with Alt Text (Letter or Index Number)\n")
        self.linkColumn = raw_input("Enter Excel Column with URL (Letter or Index Number)\n")

        super(genericEmailBuilder, self).__init__(crf_file, source_images, emailName)