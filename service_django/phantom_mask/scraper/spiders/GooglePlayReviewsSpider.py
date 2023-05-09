import scrapy


class GooglePlayReviewsSpider(scrapy.Spider):
    name = "googleplay_reviews"
    start_urls = [
        'https://play.google.com/store/apps/details?id=com.whatsapp&showAllReviews=true',
    ]

    def parse(self, response):
        # print("====response", response.text)
        for review in response.css('div.single-review'):
            print(review)
            # yield {
            #     'author': review.css('span.author-name span::text').get(),
            #     'rating': review.css('div.tiny-star')[0].attrib['aria-label'][6:7],
            #     'review': review.css('span.review-body span::text').get(),
            # }
