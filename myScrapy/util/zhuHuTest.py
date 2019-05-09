

import re
import requests
import http.cookiejar as cookielib


agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
     "User-Agent":agent
}
session=requests.session()
session.cookies=cookielib.LWPCookieJar(filename="zhihu.txt")
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("cookie未能加载")

def get_index():
    response=session.get("https://www.zhihu.com",headers=header)
    with open("index_page.html","wb") as f:
        f.write(response.text.encode("utf8"))

def get_xsrf():
    response = requests.get("https://www.zhihu.com" ,headers = header)
    print(response.text)
    match_obj = re.match('.*name="_xsrf value="(.*?)"' ,response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

def zhihu_login(account,password):
    if re.match("^1\d{10}",account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
        post_data = {
          "_xsrf": get_xsrf(),
          "phone_num" : account,
          "password" : password
        }
        resqonse_test=session.post(post_url,data=post_data,headers=header)
        session.cookies.save()
def get_c():
    import time
    t = str(int())


zhihu_login("17306646450","139742685")
# get_index()