import scrapy

from scrapy.http import Request,FormRequest
import urllib.request

class DbSpider(scrapy.Spider):
    name = "db"
    allowed_domains = ["douban.com"]
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"}

    def start_requests(self):
        return [Request("https://accounts.douban.com/login",
                        callback=self.parse,
                        meta={
                            "cookiejar":1
                        })]
    def parse(self, response):
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract()
        print("以下是验证码id号获取")
        id_value = response.xpath('/input[@name="captcha-id"]/@value').extract()
        print(id_value)
        if len(captcha)>0:
            print("此时有验证码")
            localpath = "D:/douban/captchar.jpg"
            urllib.request.urlretrieve(captcha[0],filename=localpath)
            print("请查看本地验证码图片并且输入验证码")
            captcha_value = input()

            data = {
                "form_email":"879303561@qq.com",
                "form_password":"Ljj281150",
                "redir":"https://www.douban.com/people/63369571/",
                "captcha-solution":str(captcha_value),
                "source":None,
                "captcha_valid":str(id_value),
                "login":"登录",
            }
        else:
            print("此时没有验证码")
            data={
                "form_email": "879303561@qq.com",
                "form_password": "Ljj281150",
                "redir": "https://www.douban.com/people/63369571/",
            }
        print("登陆中..........................................")
        return [FormRequest.from_response(response,
                                          meta={"cookiejar": response.meta["cookiejar"]},
                                          headers=self.headers,
                                          formdata=data,
                                          callback=self.next,
                                          )]

    def next(self, response):
        print("此时已经登录完成并且抓取了个人中心的数据")
        title = response.xpath("/html/head/title/text()").extract()
        print(title[0])






