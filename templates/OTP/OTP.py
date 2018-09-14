from distutils.dir_util import copy_tree
from shutil import copyfile
import pyexcel as p
from emailBuildClass import emailBuilder
# Needed for automatically sending tests in Mailchimp
#import mailChimp
#import os

class OTPBuilder(emailBuilder):
    def __init__(self, crf_file, source_images, emailName):
        self.projectNamePrefix = "OTP_"
        self.folderPath = "otp"
        self.ymlTemplate = "OTP/OTP_Template_053017.yml"
        self.erbTemplate = "OTP/OTP_Template_053017.erb"

        self.sheet = raw_input("Enter Excel Sheet Name with Email Data\n")
        self.altTextColumn = raw_input("Enter Excel Column with Alt Text (Letter or Index Number)\n")
        self.linkColumn = raw_input("Enter Excel Column with URL (Letter or Index Number)\n")

        super(genericEmailBuilder, self).__init__(crf_file, source_images, emailName)