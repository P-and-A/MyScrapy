# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import http.cookiejar as cookielib

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    header = {
        "HOST":"www.zhihu.com",
        "Referer":"https://www.zhihu.com",
        "User-Agent":agent
    }
    session=requests.session()
    session.cookies=cookielib.LWPCookieJar(filename="zhihu.txt")

    def get_xsrf(self):
        response = requests.get("https://www.zhihu.com",headers = self.header)
        print(response.text)
        match_obj = re.match('.*name="_xsrf value="(.*?)"',response.text)
        if match_obj:
            return (match_obj.group(1))
        else:
            return ""

    def zhihu_login(self,account,password):
        if re.match("^1\d{10}",account):
            print("手机号码登录")
            post_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
            post_data = {
                "_xsrf": self.get_xsrf,
                "phone_num" : account,
                "password" : password

            }
            resqonse_test=self.session.post(post_url,data=post_data,headers=self.header)
            self.session.cookies.save()
        pass

    def parse(self, response):
        pass
