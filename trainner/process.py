import os
import re
from db.mongo import UrlTrainModel
import idna
import tldextract
import editdistance
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer


class Profile():
    url = None
    len_url = None
    is_spec_url = None
    is_uni_subdomain = None

    num_a = None
    num_a_null = None

    host_similar = None
    is_title_kw = None
    len_txt_vis = None
    txt_similar = None
    num_txt_kw = None

    num_img = None
    num_img_sim = None
    size_res = None
    num_domain_protect = None
    txt_visible = None
    title = None

    def __init__(self, url, path_data):
        self.url = url
        self.path_data = path_data
        self.init_data()
        self.init_url()

    def init_url(self):
        url_ex = tldextract.extract(self.url)
        host = url_ex.subdomain + "." + url_ex.domain
        self.len_url = len(self.url)
        self.is_spec_url = self.is_special_url(self.url)
        self.is_uni_subdomain = self.is_uni(host)

    def init_data(self):
        path_html = self.path_data + "/" + "content.html"
        f_html = open(path_html)
        f_html.tell()
        self.size_res = os.path.getsize(path_html)
        self.soup = BeautifulSoup(f_html)
        list_text = filter(self.visible, self.soup.findAll(text=True))
        title_elment = self.soup.title
        if title_elment is not None:
            self.title = title_elment.string.lower()
        else:
            self.title = ""
        list_tag_a = self.soup.findAll("a")
        self.num_a = len(list_tag_a)
        self.num_a_null = 0
        for tag_a in list_tag_a:
            if "href" not in tag_a.attrs or tag_a.attrs["href"].startswith("#"):
                self.num_a_null += 1
        self.num_img = len(self.soup.findAll("img"))

        self.txt_visible = ''
        self.len_txt_vis = 0
        for item in list_text:
            line = re.sub(" +", " ", item.strip())
            if len(line) > 0:
                self.len_txt_vis += len(line)
                self.txt_visible += " " + line

    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        return True

    def is_special_url(self, url):
        special_list = [
            "@", "<script"
        ]
        for item in special_list:
            if item in url:
                return 1
        return 0

    def is_uni(self, subdomain):
        if subdomain != idna.decode(subdomain):
            return 1
        else:
            return 0

    def set_is_title_con_kw(self, list_kw):
        for item in list_kw:
            if item in self.title:
                self.is_title_kw = 1
                return
        self.is_title_kw = 0

    def set_similar_text(self, text_compare):
        vect = TfidfVectorizer()
        tfidf = vect.fit_transform([self.txt_visible, text_compare])
        self.txt_similar = (tfidf * tfidf.T).A[0, 1]

    def set_host_similar(self, url_compare):
        ex_self = tldextract.extract(self.url)
        if len(ex_self) > 0:
            host_self = ex_self.subdomain + "." + ex_self.domain
        else:
            host_self = ex_self.domain
        ex_compare = tldextract.extract(url_compare)
        if len(ex_self) > 0:
            host_compare = ex_compare.subdomain + "." + ex_compare.domain
        else:
            host_compare = ex_compare.domain
        self.host_similar = 1 - (
            1.0 * editdistance.eval(host_self, host_compare) / max(len(host_compare), len(host_self)))

    def set_txt_kw(self, list_kw):
        contents = open(self.path_data + "/" + "content.html").read()
        self.num_txt_kw = 0
        for item in list_kw:
            self.num_txt_kw += contents.count(item)

    def set_num_domain_protect(self, url):
        register_domain = tldextract.extract(url).registered_domain
        contents = open(self.path_data + "/" + "content.html").read()
        self.num_domain_protect = contents.count(register_domain)

        # list_tag_a = self.soup.findAll("a")
        # for item in list_tag_a:
        #     if "href" in item.attrs and tldextract.extract(item.attrs["href"]).registered_domain == register_domain:
        #         self.num_domain_protect += 1

    def get_json_attrs(self):
        return {
            UrlTrainModel.LEN_URL: self.len_url,
            UrlTrainModel.IS_SPEC_URL: self.is_spec_url,
            UrlTrainModel.IS_UNI_SUB: self.is_uni_subdomain,
            UrlTrainModel.NUM_A: self.num_a,
            UrlTrainModel.NUM_A_NULL: self.num_a_null,
            UrlTrainModel.NUM_IMG: self.num_img,
            UrlTrainModel.HOST_SIMILAR: self.host_similar,
            UrlTrainModel.IS_TITLE_KW: self.is_title_kw,
            UrlTrainModel.LEN_TXT_VIS: self.len_txt_vis,
            UrlTrainModel.TXT_SIMILAR: self.txt_similar,
            UrlTrainModel.NUM_TXT_KW: self.num_txt_kw,
            UrlTrainModel.SIZE_RES: self.size_res,
            UrlTrainModel.NUM_DOMAIN_PROTECT: self.num_domain_protect
        }


class RawProcessor():
    path_data = "/media/thangld/000970C6000D80A3/Project/viettel/data_crawl/url_train"

    def __init__(self):
        pass

    def update_attr(self):
        url_model = UrlTrainModel()
        fb_profile = Profile("https://www.facebook.com/login.php?login_attempt=1&lwv=110",
                             "/media/thangld/000970C6000D80A3/Project/viettel/data_crawl/profile/facebook/www.facebook.com_0")
        data = url_model.collect_model.find(

            {
                # "facebook": {"$exists": False},
                url_model.DATA: {"$exists": True},
            }
        )
        count = 0
        for site in data:
            count += 1
            print count
            url = site[url_model.URL]
            path = self.path_data + "/" + site[url_model.DATA]
            if not os.path.exists(path):
                continue
            site_profile = Profile(url, path)
            site_profile.set_is_title_con_kw(["facebook"])
            site_profile.set_similar_text(fb_profile.txt_visible)
            site_profile.set_host_similar(fb_profile.url)
            site_profile.set_num_domain_protect(fb_profile.url)
            site_profile.set_txt_kw(["facebook"])
            url_model.collect_model.update_one(
                {
                    url_model.URL: url
                },
                {
                    "$set": {
                        "facebook": site_profile.get_json_attrs()
                    }
                }
            )
            # break


raw_processor = RawProcessor()
raw_processor.update_attr()
