# -*- coding: utf-8 -*-
import scrapy

from BooksFromSpider.BooksFromSpider.items import BooksfromspiderItem as Item


class BookspiderSpider(scrapy.Spider):
    name = 'BookSpider'
    allowed_domains = ['github.com']

    start_urls = ['https://github.com/search?q=book', 'https://github.com/search?q=books',
                  "https://github.com/search?q=%E4%B9%A6%E5%8D%95", "https://github.com/search?q=booklist"
                  ]
    targetUrls = ['https://github.com/search?q=book',
                  'https://github.com/search?q=books',
                  "https://github.com/search?q=%E4%B9%A6%E5%8D%95",
                  "https://github.com/search?q=booklist"]

    allowedFileSuffix = ["pdf", "epub", "mobi"]
    bannedFileName = ["readme", "README"]

    def __init__(self, **kwargs):
        # 爬取一百頁
        super().__init__(**kwargs)
        for i in range(1, 30):
            for url in self.targetUrls:
                self.start_urls.append(url + "&p=" + str(i))

    def parse(self, response):
        # 搜查book的結果
        if response.url in self.targetUrls:
            repositoryLiList = response.xpath("//ul[@class='repo-list']/li")
            for repositoryLi in repositoryLiList:
                # # 取得倉庫名稱
                # repositoryName = "".join(repositoryLi.xpath("./div/h3/a").xpath("string(.)").extract()).strip()
                # # print(repositoryName)

                # 取得倉庫連結
                repositoryURL = "".join(repositoryLi.xpath("./div/h3/a/@href").extract()).strip()
                # print(repositoryURL)

                # # 取得倉庫描述
                # repositoryDescription = "".join(repositoryLi.xpath("./div/p").xpath("string(.)").extract()).strip()
                # # print(repositoryDescription)
                #
                # # 取得倉庫star
                # repositoryStars = "".join(repositoryLi.xpath("./div[2]/div[2]/a/text()").extract()).strip()
                # # print(repositoryStars)

                yield scrapy.Request("http://github.com" + repositoryURL, callback=self.parse)
        else:  # 倉庫詳細頁
            repositoryBody = response.xpath("//tbody/tr")
            repositoryBody.pop(0)  # 第一個td不是想要的
            repositoryName = "".join(response.xpath("//main/div/div/h1").xpath("string(.)").extract()).strip()
            # repositoryDescription = "".join(response.xpath("//main/div[2]/div/div/div/span").xpath("string(.)").extract()).strip()
            # repositoryStars = "".join(response.xpath("//main/div/div/ul/li[2]/div/form[2]/a").xpath("string(.)").extract()).strip()
            bookList = []
            # print(repositoryName)
            for tdTag in repositoryBody:
                isDirectory = "directory" == "".join(
                    tdTag.xpath("./td[@class='icon']/svg/@aria-label").extract()).strip()
                bookURL = "".join(
                    tdTag.xpath("./td[@class='content']/span/a/@href").extract()).strip()
                if isDirectory is False:
                    bookName = "".join(tdTag.xpath("./td[@class='content']").xpath("string(.)").extract()).strip()
                    split = bookName.split(".")
                    if len(split) < 2 or split[1] not in self.allowedFileSuffix or split[1] in self.bannedFileName:
                        continue

                    bookList.append({"name": bookName, "url": "http://github.com" + bookURL})
                else:  # 是一個目錄，假䛇打開該目錄後的頁面結構與上面相同
                    print(bookURL)
                    yield scrapy.Request("http://github.com" + bookURL)
            item = Item()
            item["bookList"] = bookList
            item["repositoryName"] = repositoryName
            item["repositoryURL"] = response.url
            if len(bookList) != 0:
                yield item
        pass
