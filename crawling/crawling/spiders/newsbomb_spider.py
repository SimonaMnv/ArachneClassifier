from crawling.items import ArticleItem
import scrapy
import json
import re


def check_type(keywords):
    if "ΝΑΡΚΩΤ" in keywords:
        return "ΝΑΡΚΩΤΙΚΑ"
    elif "ΔΟΛΟΦΟΝ" in keywords:
        return "ΔΟΛΟΦΟΝΙΑ"
    elif "ΛΗΣΤ" in keywords or "ΚΛΟΠ" in keywords:
        return "ΛΗΣΤΕΙΑ/ΚΛΟΠΗ"
    elif "ΒΙΑΣ" in keywords or "ΠΑΙΔΕΡΑ" in keywords or "ΠΑΙΔΟΦΙΛ" in keywords or "ΣΕΞΟΥΑΛΙΚ" in keywords:
        return "ΣΕΞΟΥΑΛΙΚΟ ΕΓΚΛΗΜΑ"
    elif "ΤΡΟΜΟΚΡΑΤ" in keywords:
        return "ΤΡΟΜΟΚΡΑΤΙΚΗ ΕΠΙΘΕΣΗ"
    else:
        return "ΑΛΛΟ ΕΓΚΛΗΜΑ"


def check_scope(keywords):
    if 'ΕΛΛΑΔΑ' in keywords:
        return "ΕΛΛΑΔΑ"
    else:
        return "ΚΟΣΜΟΣ"


class NewsbombSpider(scrapy.Spider):
    name = 'newsbomb'
    allowed_domains = ['newsbomb.gr']
    start_urls = ['https://www.newsbomb.gr/ellada/astynomiko-reportaz', 'https://www.newsbomb.gr/tag/dolofonia',
                  'https://www.newsbomb.gr/tag/lhsteia', 'https://www.newsbomb.gr/tag/kloph',
                  'https://www.newsbomb.gr/tag/viasmos', 'https://www.newsbomb.gr/tag/narkwtika',
                  'https://www.newsbomb.gr/tag/paiderastia', 'https://www.newsbomb.gr/tag/tromokratikh-epithesh',
                  'https://www.newsbomb.gr/tag/apagwgh', 'https://www.newsbomb.gr/tag/sexoyalika-egklhmata',
                  'https://www.newsbomb.gr/tag/paidofiloi']

    def parse(self, response):
        article_links = response.css('a.overlay-link ::attr(href)')

        for link in article_links:
            url = 'https://www.newsbomb.gr' + link.get()
            print("URL", url)
            yield scrapy.Request(url=url, callback=self.parse_article)

        original_url = re.findall(r'[^?]*', str(response.url))
        next_page = str(original_url[0]) + "?page=" + str(
            int(response.css("span.nav-page span.nav-number::text").get()) + 1)
        if next_page:
            print("turned to page", next_page)
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        article = ArticleItem()

        article['title'] = data["@graph"][0]["headline"]
        article['date'] = data["@graph"][0]["datePublished"]
        article['body'] = data["@graph"][0]["articleBody"]
        article['tags'] = data["@graph"][0]["keywords"]
        article['author'] = data["@graph"][0]["author"]['name']
        article['link'] = data["@graph"][0]["mainEntityOfPage"]["@id"]
        article['type'] = check_type(article['tags'])
        article['scope'] = check_scope(article['tags'])

        yield article

# 1. to scrape: go in crawling>crawling: scrapy crawl newsbomb
# 2. to check the html manually before parsing: scrapy shell > fetch(site) > print(response.text)
