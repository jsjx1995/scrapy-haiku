import scrapy


class HaikuSpiderSpider(scrapy.Spider):
    name = 'haiku_spider'
    allowed_domains = ['kigosai.sub.jp']
    start_urls = [
        'https://kigosai.sub.jp/001/%e5%9f%ba%e6%9c%ac%e5%ad%a3%e8%aa%9e700']

    def parse(self, response):
        kigosai_url = "https://kigosai.sub.jp/001/archives"
        anchor_links = response.selector.xpath(
            '//a')
        f'//a[contains(@href, {kigosai_url})]/@href').getAll()
        for anchor_link in anchor_links:

            url=anchor_link.xpath('@href').get()
            text=anchor_link.xpath('text()').get()
            if kigosai_url in url:
                request=scrapy.Request(
                    url, callback = self.parse2, cb_kwargs = dict(text=text))
                yield request

    def parse2(self, response, text):
        # yield {'anchor_link': anchor_link.xpath('text()').get()}
        texts=response.xpath('//p[1]/text()')
        # print(texts[1].get())
        kokigo=''
        explanation=''
        related=''
        history=''
        example=''
        for i in range(len(texts)):
            if '【子季語】' in texts[i].get():
                kokigo=texts[i + 1].get()
            if '【解説】' in texts[i].get():
                explanation=texts[i + 1].get()
            if '【関連季語】' in texts[i].get():
                related=texts[i + 1].get()
            if '【来歴】' in texts[i].get():
                history=texts[i + 1].get()
            if '【例句】' in texts[i].get():
                example=texts[i + 1].get()

        yield dict(
            text=text,
            kokigo=kokigo,
            explanation=explanation,
            related=related,
            history=history,
            example=example
        )

