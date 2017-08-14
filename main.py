from db.mongo import UrlTrainModel


#
#
# import tldextract
# item = tldextract.extract("https://coinline907.000webhostapp.com/phoneUS/facebook=bd4b26676e6741fb1riko.html")
# print item

def update_type():
    url_model = UrlTrainModel()

    # data = url_model.collect_model.find({})
    # for site in data:


    #
    #     if "data" in site and site["data"].startswith("phishing_facebook"):
    #         url_model.collect_model.update_one(
    #             {
    #                 url_model.URL:site["url"]
    #             },
    #             {
    #                 "$set":{
    #                     url_model.TYPE:{
    #                         url_model.IS_PHISHING: url_model.TYPE_VALUES["phishing"],
    #                         url_model.TARGET: url_model.TARGET_PHISHING_VALUES["facebook"],
    #                     }
    #                 }
    #             }
    #         )

    # f = open("./data/login_benign.txt")
    # count = 0
    # for item in f:
    #     url = item.strip()
    #     if url_model.collect_model.find_one({UrlTrainModel.URL: url}) is None:
    #         count += 1
    #         print count
    #         url_model.collect_model.insert_one(
    #             {
    #                 UrlTrainModel.URL: url,
    #                 UrlTrainModel.TYPE: {
    #                     UrlTrainModel.IS_PHISHING: UrlTrainModel.TYPE_VALUES["benign"],
    #                     # UrlTrainModel.TARGET: UrlTrainModel.TARGET_PHISHING_VALUES["other"]
    #                 }
    #             }
    #         )


def insert():
    url_model = UrlTrainModel()
    f = open("./data/login_benign.txt")
    for url in f:
        url = url.strip()
        if url_model.collect_model.find_one({UrlTrainModel.URL: url}) is None:
            url_model.collect_model.insert_one(
                {
                    UrlTrainModel.URL: url,
                    UrlTrainModel.TYPE: {
                        UrlTrainModel.IS_PHISHING: UrlTrainModel.TYPE_VALUES["benign"]
                    }
                }
            )
    print "finish"


update_type()
