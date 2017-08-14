import os
import scrapy
from scrapy_splash import SplashRequest
import base64
import tldextract
# from TrainPhishing.db.mongo import UrlModel
from db.mongo import UrlTrainModel
import imp


# foo = imp.load_source('module.name', '../db/monogo.py')
# 173566

class QuotesSpider(scrapy.Spider):
    name = "benign"
    type = "phishing_other"
    path_collection = "/media/thangld/000970C6000D80A3/Project/viettel/data_crawl/url_train"
    path_save_type = path_collection + "/" + type

    def start_requests(self):
        if not os.path.exists(self.path_save_type):
            os.mkdir(self.path_save_type)

        urls = []

        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
            'wait': 10  # S
        }

        url_model = UrlTrainModel()

        pipeline = [
            {"$match":
                 {UrlTrainModel.TYPE + "." + UrlTrainModel.IS_PHISHING: UrlTrainModel.TYPE_VALUES["phishing"],
                  UrlTrainModel.TYPE + "." + UrlTrainModel.TARGET: UrlTrainModel.TARGET_PHISHING_VALUES["other"],
                  }
             },

            # {"$limit":10}
        ]
        data = url_model.collect_model.aggregate(pipeline)
        for item in data:
            urls.append(item["url"])
            print item["url"]
        print "{} {}".format("number", len(urls))
        for url in urls:
            yield SplashRequest(url, self.parse_res, method="GET", endpoint="render.json",
                                args=splash_args)

    def parse_res(self, response):
        self.log(response.url)
        status_code = response.status
        if status_code != 200:
            return
        url = response.url
        if url.startswith("http://"):
            url_removed_prefix = url[7:]
        elif url.startswith("https://"):
            url_removed_prefix = url[8:]
        pos = url_removed_prefix.find("/")
        sub_domain = url_removed_prefix[:pos]

        # if status_code == 200:
        self.log("save file")
        res_body = response.body
        path_origin = self.path_save_type + "/" + sub_domain
        index = 0;
        path = path_origin + "_" + str(index)
        while os.path.exists(path):
            index += 1
            path = path_origin + "_" + str(index)
        os.makedirs(path)
        html_file = path + '/content.html'
        with open(html_file, 'wb') as f:
            f.write(res_body)

        png_file = path + "/img.png"
        with open(png_file, "wb") as f_img:
            f_img.write(base64.b64decode(response.data['png']))

        url_model = UrlTrainModel()
        url_model.collect_model.update_one(
            {
                UrlTrainModel.URL: url
            },
            {
                "$set": {
                    UrlTrainModel.DATA: path.replace(self.path_collection + "/", ""),
                    UrlTrainModel.SIZE_RES: len(res_body)
                }
            }
        )
        # else:
        #     print "fail"
        # url_model.collect_model.delete_one(
        #     {
        #         UrlTrainModel.URL: url
        #     }
        # )

        # def parse_result(self, response):
        #     # magic responses are turned ON by default,
        #     # so the result under 'html' key is available as response.body
        #     html = response.body
        #
        #     # you can also query the html result as usual
        #     title = response.css('title').extract_first()
        #
        #     # full decoded JSON data is available as response.data:
        #     png_bytes = base64.b64decode(response.data['png'])
