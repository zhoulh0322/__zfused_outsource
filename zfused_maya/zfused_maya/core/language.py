# coding:utf-8
# --author-- lanhua.zhou

import os
import json

import zfused_maya

__all__ = ["word"]

ZH_CN_JSON = zfused_maya.setup_resource().get("zh_cn", "language.json")
EN_US_JSON = zfused_maya.setup_resource().get("en_us", "language.json")

LANGUAGE_JSON = {
    "zh_cn": ZH_CN_JSON,
    "en_us": EN_US_JSON
}

class Language(object):
    LANGUAGE = "zh_cn"
    with open(LANGUAGE_JSON[LANGUAGE], "rb") as _file_handle:
        LANGUAGE_DATA = json.loads(_file_handle.read())

    def set_language(self, language):
        self.LANGUAGE = language
        with open(LANGUAGE_JSON[self.LANGUAGE], "rb") as _file_handle:
            self.LANGUAGE_DATA = json.loads(_file_handle.read())

def word(language_code):
    return u"{}".format(Language.LANGUAGE_DATA[language_code])


if __name__ == "__main__":
    print(word("project setting"))