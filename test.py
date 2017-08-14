from db.mongo import UrlTrainModel


def insert():
    url_model = UrlTrainModel()
    f = open("./data/fb_phishing.txt")
    for url in f:
        url = url.strip()
        url_model.collect_model.insert_one(
            {
                UrlTrainModel.URL: url
            }
        )
    print "finish"


def update_type():
    url_model = UrlTrainModel()

    url_model.collect_model.update(
        {},
        {"$set": {
            UrlTrainModel.TYPE:
                {
                    UrlTrainModel.TYPE: UrlTrainModel.TYPE_VALUES["phishing"],
                    UrlTrainModel.TARGET: UrlTrainModel.TARGET_PHISHING_VALUES["facebook"]
                }
        }
        }

    )


update_type()
