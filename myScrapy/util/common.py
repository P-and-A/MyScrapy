import hashlib
import os
import re

import MySQLdb

import myScrapy
from datetime import datetime
from myScrapy.settings  import SQL_DATETIME_FORMAT

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums



def salary_possessor(value):
    re_object = re.match(r'^(\d+)[kK]-(\d+)[kK].*', value)
    if re_object:
        return int(re_object.group(1))*1000, int(re_object.group(2))*1000
def work_year_possessor(value):
    re_object = re.match(r'^经验(\d+)-(\d+年).+', value)
    if re_object:
        return re_object.group(1)+"年", re_object.group(2)
    elif re.match(r"经验应届毕业生",value):
        return "经验应届毕业生","经验应届毕业生"
    else:
        return "经验不限", "经验不限"

def degree_need_processor(value):
    re_object = re.match(r'(.*)及.*', value)
    if re_object:
        return re_object.group(1)
    else:
        return '学历不限'


def add_processor(value):
    value = value.replace(" ","")
    return value.replace("查看地图", "")

def time_processor(value):
    time1 = re.match(r'(\d{4}-\d{2}-\d{2}).*发布.*',value)
    time2 = re.match(r'(\d{2}.?\d{2}).*发布.*',value)
    if time1:
        return time1.group(1)
    elif time2:
        return datetime.now().strftime(myScrapy.settings.SQL_DATETIME_FORMAT) + time2.group(1)

def write_number(number):
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) +'\scrapy.txt'
    try:
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(number)

    except:
        print('写入失败')

def read_number():
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) +'\scrapy.txt'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            a = f.read()
            return a
    except:
        print('读取失败')

def write_and_read():
    i = int(read_number()) + 1
    write_number(str(i))
    print(i)
    return i

def my_select_row():
    # 第二个参数：连接用户名，3：密码，4：数据库             ！！！需存在被查询的表
    db = MySQLdb.connect("localhost", "root", "root", "recruitment", charset='utf8')
    cusor = db.cursor()
    cusor.execute("select tags from lagou_job " )
    return cusor.fetchall()

if __name__ == "__main__":
    print (get_md5("http://jobbole.com".encode("utf-8")))