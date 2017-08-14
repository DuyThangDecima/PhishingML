from pymongo import *
from config import *


class ColectModel():
    collect_name = None
    collect_model = None
    db = None

    def __init__(self):
        self.client = MongoClient(DB_HOST, DB_PORT)
        self.db = self.client[DB_NAME]
        self.collect_model = self.db[self.collect_name]
        return


class UrlTrainModel(ColectModel):
    """
    """
    # LOGIN = "login"
    # IS_LOGIN = "is_login"
    # SUB_DOMAIN = "sub-domain"
    # LOGIN_TYPE = "login_type"
    # DETECTOR = "detector"
    # RESULT = "result"
    # VERIFY = "verify"
    # TIME_STAMP_INSERT = "time_stamp_insert"
    # POINT = "point"
    # GOOGLE_SAFE_BROWSING = "google_safe_browsing"
    # THREAD_TYPE_VALUES = {
    #     "MALWARE": "MALWARE",
    #     "SOCIAL_ENGINEERING": "SOCIAL_ENGINEERING",
    #     "UNWANTED_SOFTWARE": "UNWANTED_SOFTWARE",
    #     "POTENTIALLY_HARMFUL_APPLICATION": "POTENTIALLY_HARMFUL_APPLICATION"
    # }
    # STATUS_CODE = "status_code"
    # IS_DETECT = "is_detect"
    # THREAD_TYPE = "thread_type"

    collect_name = "url_ml"

    IS_PHISHING = "is_phishing"

    # ----- THUOC TINH URL ----------
    URL = "url"
    LEN_URL = "len_url"
    URL_CHAR_SPEC = "url_char_spec"
    SUB_CON_NUM = "sub_con_num"

    # ----- THUOC TINH HMTL ----------
    NUM_A = "num_a"
    NUM_A_NULL = "num_a_null"

    SUB_SIMILAR = "sub_similar"

    TITLE_CON_DOMAIN = "title_con_domain"

    BACKGROUND_COLOR = "background_color"
    FOREGROUND_COLOR = "foreground_color"

    LEN_TXT_VIS = "len_txt_vis"
    TXT_SIMILAR = "txt_similar"
    TXT_KW = "txt_kw"

    # THUOC TINH ICON, LOGO
    NUM_IMG = "num_img"
    NUM_IMG_SIM = "num_img_sim"

    # TITLE_CON_KW = "title_con_kw"
    # SUB_KW = "sub_kw"
    # URI_KW = "uri_kw"

    COUNT = "count"
    DATA = "data"
    SIZE_RES = "size_res"
    TARGET = "target"
    TYPE = "type"

    VERIFY_VALUES = {
        "finished": 1,
        "unfinished": -1,
        "analysing": 0
    }

    TYPE_VALUES = {
        "unknown": -1,
        "phishing": 1,
        "benign": 0,
    }

    TARGET_PHISHING_VALUES = {
        "facebook": 1,
        "gmail": 2,
        "garena": 3,
        "vtc": 4,
        "other": 5
    }
