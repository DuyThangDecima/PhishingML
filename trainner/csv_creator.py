from db.mongo import UrlTrainModel
import csv


class CsvCreator():
    def create_csv(self):
        url_model = UrlTrainModel()

        list_site = url_model.collect_model.find(
            {
                "facebook": {"$exists": True},
                UrlTrainModel.TYPE + "." + UrlTrainModel.IS_PHISHING: url_model.TYPE_VALUES["phishing"],
                UrlTrainModel.TYPE + "." + UrlTrainModel.TARGET: url_model.TARGET_PHISHING_VALUES["facebook"],
            }
        )
        type = 0
        file_csv = open("../data/attr_classify.csv", "w+")
        writer = csv.writer(file_csv)
        for data in list_site:
            list_val = self.get_list_val(data)
            list_val.append(type)
            writer.writerow(list_val)

        type = 1
        list_site = url_model.collect_model.find(
            {
                "facebook": {"$exists": True},
                UrlTrainModel.TYPE + "." + UrlTrainModel.IS_PHISHING: url_model.TYPE_VALUES["benign"],
                # UrlTrainModel.TYPE + "." + UrlTrainModel.TARGET: url_model.TARGET_PHISHING_VALUES["facebook"],
            }
        )
        for data in list_site:
            list_val = self.get_list_val(data)
            list_val.append(type)
            writer.writerow(list_val)

        list_site = url_model.collect_model.find(
            {
                "facebook": {"$exists": True},
                UrlTrainModel.TYPE + "." + UrlTrainModel.IS_PHISHING: url_model.TYPE_VALUES["phishing"],
                UrlTrainModel.TYPE + "." + UrlTrainModel.TARGET: url_model.TARGET_PHISHING_VALUES["other"],
            }
        )
        for data in list_site:
            list_val = self.get_list_val(data)
            list_val.append(type)
            writer.writerow(list_val)

    def get_list_val(self, data):
        len_url = data["facebook"][UrlTrainModel.LEN_URL]
        is_spec_url = data["facebook"][UrlTrainModel.IS_SPEC_URL]
        is_uni_subdomain = data["facebook"][UrlTrainModel.IS_UNI_SUB]
        num_a = data["facebook"][UrlTrainModel.NUM_A]
        num_a_null = data["facebook"][UrlTrainModel.NUM_A_NULL]
        num_img = data["facebook"][UrlTrainModel.NUM_IMG]
        host_similar = data["facebook"][UrlTrainModel.HOST_SIMILAR]
        is_title_kw = data["facebook"][UrlTrainModel.IS_TITLE_KW]
        len_txt_vis = data["facebook"][UrlTrainModel.LEN_TXT_VIS]
        txt_similar = data["facebook"][UrlTrainModel.TXT_SIMILAR]
        num_txt_kw = data["facebook"][UrlTrainModel.NUM_TXT_KW]
        size_res = data["facebook"][UrlTrainModel.SIZE_RES]
        num_domain_protect = data["facebook"][UrlTrainModel.NUM_DOMAIN_PROTECT]
        list_val = []
        list_val.extend([len_url, is_spec_url, is_uni_subdomain, num_a, num_a_null,
                         num_img, host_similar, is_title_kw, len_txt_vis, txt_similar,
                         num_txt_kw, size_res, num_domain_protect])
        return list_val


train = CsvCreator()
train.create_csv()