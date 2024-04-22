import scrapy
#scrapy runspider crawler.py -o output.json
class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia_spider'
    start_urls = ['https://en.wikipedia.org/wiki/Sport']
    custom_settings = {
            "DEPTH_LIMIT": 2,
            "PAGE_LIMIT" : 100
        }
   
    def __init__(self, *args, **kwargs):
        super(WikipediaSpider, self).__init__(*args, **kwargs)
        self.page_count = 0

    def parse(self, response):
        # Extracting links to articles from the main page
        article_links_Fulllist = response.css('a::attr(href)').getall()
        getwikiLinks = lambda x : x[0:6] == '/wiki/' and not ":" in x
        article_links_temp = list(filter(getwikiLinks , article_links_Fulllist))
        
        for link in article_links_temp:
            self.page_count +=1 
            if self.page_count < self.custom_settings['PAGE_LIMIT']:
                self.logger.info(f"pagecount {self.page_count}")
                yield response.follow(link, callback=self.parse_article, meta={'depth': 1})

    def parse_article(self, response):
        # Extracting desired content from the article page
        title_tag = response.xpath('//title/text()').get()
        divs = response.xpath("//div")
        content = ""
        for p in divs.xpath(".//p"):
            # Extracting text content including <a> tags
            text_content_with_links = ''.join(p.xpath("string()").getall())
            content += " " + text_content_with_links + " "

        current_link = response.url
        
        
        # if self.page_count > self.custom_settings['PAGE_LIMIT']:
        #     return
        yield {
            'link': current_link,
            'title': title_tag,
            'content': content
        }


        # Extracting links to other articles and following them recursively
        if response.meta['depth'] < self.custom_settings['DEPTH_LIMIT'] and self.page_count < self.custom_settings['PAGE_LIMIT']:
            article_links_Fulllist = response.css('a::attr(href)').getall()
            getwikiLinks = lambda x: x[0:6] == '/wiki/' and not ":" in x
            article_links_temp = list(filter(getwikiLinks, article_links_Fulllist))

            for link in article_links_temp:
                yield response.follow(link, callback=self.parse_article, meta={'depth': response.meta['depth'] + 1})
