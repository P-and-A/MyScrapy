# -*- coding: utf-8 -*-
import datetime
import hashlib
import re

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from myScrapy.util.common import get_md5, my_select_row, read_number, write_and_read
from myScrapy.items import LagouJobItem, LagouJobItemLoader, LagouSortItem, ArticlespiderItem
from datetime import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    i = write_and_read()
    start_urls = [my_select_row()[i][3]]
    third_title = my_select_row()[i][2]
    second_title = my_select_row()[i][1]
    first_title = my_select_row()[i][0]
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
        }
    }
    rules = (
        Rule(LinkExtractor(allow=(re.match(r".*(zhaopin/.*/).*", my_select_row()[int(read_number())][3]).group(1) + ".*")),
             follow=True),
        # Rule(LinkExtractor(allow=("gongsi/j\d+.html")),follow=True),

        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=False),
        # Rule(LinkExtractor(allow=r'jobs/4209470.html'), callback='parse_job', follow=True),
    )
    # def parse_zhaoping(self, response):
    #     item_loader = LagouJobItemLoader(item=LagouSortItem,respons=response)
    #     item_loader.add_css("first_title","'.category-list h2::text'")
    #     item_loader.add_css("second_title",".menu_sub dl dt span::text")
    #     item_loader.add_css("third_title",".curr::text")
    #     zhaoping_item=item_loader.load_item()
    #     return zhaoping_item
    def parse_start_url(self, response):
        # a = response.xpath("//div[@class='mainNavs']//div[contains(@class,'menu_sub')]//a")
        # # a=response.css(".mainNavs a")
        # for b in a:
        #     url = b.xpath("./@href")
        #     third_title=b.xpath("./text()")
        #     second_title=b.xpath("../..//span/text()")
        #     first_title=b.xpath("../../../..//h2/text()")
        #     item_loader = LagouJobItemLoader(item=LagouSortItem(), response=response)
        #     item_loader.add_value("first_title", first_title.extract())
        #     item_loader.add_value("second_title", second_title.extract())
        #     item_loader.add_value("third_title", third_title.extract())
        #     item_loader.add_value("url", url.extract())
        #     zhaoping_item = item_loader.load_item()
        #     u =url.extract()[0]
        #     self.first_title=first_title.extract()
        #     self.second_title=second_title.extract()
        #     self.third_title=third_title.extract()
        #     print(u)
        #     yield zhaoping_item
        #     yield Request(url=u, callback=self.parse_zhaopin)

        return []
    def parse_zhaopin(self, response):
        urls = response.css('.position_link::attr("href")').extract()
        for object_url in urls:
            yield Request(url=object_url, callback=self.parse_job)

        # 提取下一页并交给scrapy进行下载
        next_url = response.xpath("//div[@class='pager_container']/a[last()]/@href").extract_first("")
        next = response.xpath("//a[contains(@class,'page_no pager_next_disabled')]")

        if not next and next_url:
            yield Request(url=next_url, callback=self.parse_zhaopin)

    def process_results(self, response, results):
        # zhaoping_item = LagouSortItem()
        # zhaoping_item["first_title"]=response.css(".category-list h2::text")
        # zhaoping_item["second_title"] = response.css(".menu_sub dl dt span::text")
        # zhaoping_item["third_title"] = response.css(".curr::text")

        # item_loader = ArticlespiderItem(item=LagouSortItem(), response=response)
        # item_loader.add_css("first_title", ".category-list h2::text")
        # item_loader.add_css("second_title", ".menu_sub dl dt span::text")
        # item_loader.add_css("third_title", ".curr::text")
        # print(item_loader.load_item())
        # yield zhaoping_item
        return results

    def parse_job(self, response):
        #解析拉钩网职位信息
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name span::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
        if response.css('.position-label li::text'):
            item_loader.add_css("tags", '.position-label li::text')
        else:
            item_loader.add_value("tags","无")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())
        item_loader.add_value("first_title", self.first_title)
        item_loader.add_value("second_title", self.second_title)
        item_loader.add_value("third_title", self.third_title)
        item_loader.add_xpath("domain","//*[@id='job_company']/dd/ul/li[1]/text()")
        item_loader.add_xpath("company_scale","//*[@id='job_company']/dd/ul/li[2]/text()")
        item_loader.add_xpath("development_stages","//*[@id='job_company']/dd/ul/li[last()-1]/text()")
        job_item = item_loader.load_item()
        # print("first-----")
        # print(job_item)
        # print("----------------------------------------------")
        return job_item
