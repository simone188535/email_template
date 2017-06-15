import pprint
import base64
from mailchimp3 import MailChimp
import os
import zipfile

pp = pprint.PrettyPrinter(indent=4)

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()
    return zf.filename


def upload(files, title, subject_line, reply_to, from_name, recipients):

    print("Uploading {}:{}".format(title, subject_line))
    qaListId = '7983aa283a'

    archive = zip(files, title)

    campaignData = {}
    campaignData["recipients"] = {"list_id":qaListId}
    campaignData["type"] = "regular"
    campaignData["settings"] = {}
    campaignData["settings"]["subject_line"] = subject_line
    campaignData["settings"]["reply_to"] = reply_to
    campaignData["settings"]["from_name"] = from_name
    campaignData["settings"]["title"] = title

    client = MailChimp('dev@purered.net', '6f1cd2a3f088a1b1b7df482527e00dea-us12', timeout=120.0)

    clientResponse = client.campaigns.create(data=campaignData)

    with open(archive, "rb") as archive_file:
        base64File = base64.b64encode(archive_file.read())

    contentData = {}
    contentData["archive"] = {"archive_content":base64File}

    client.campaigns.content.update(campaign_id=clientResponse["id"], data=contentData)

    if os.path.isfile(archive):
        os.remove(archive)


    testData = {"test_emails":recipients,"send_type":"html"}
    client.campaigns.actions.test(campaign_id=clientResponse["id"], data=testData)

    #FOR TESTING
    #if clientResponse["id"].strip() != '' and len(clientResponse["id"]) > 4:
    #    client.campaigns.delete(campaign_id=clientResponse["id"])