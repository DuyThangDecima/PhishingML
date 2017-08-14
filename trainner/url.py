import json
path_file = "/media/thangld/000970C6000D80A3/Project/viettel/PhishingTank/verified_online.json"
data = json.load(open(path_file))
fb_url = open("/media/thangld/000970C6000D80A3/Project/viettel/PhishingTank/facebook_url.txt", "w+")
for item in data:
    if item["target"] == "Facebook":
        fb_url.write( item["url"] + "\n")