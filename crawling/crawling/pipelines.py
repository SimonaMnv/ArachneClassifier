from bson.objectid import ObjectId
from api.models.article_model import ArticleOfInterest
import re
import hashlib


class DjangoPipeline(object):
    collection_name = 'scrapy_articles'

    def process_item(self, item, spider):
        body = item["body"]

        # 1. remove junk sentences from body
        body_junkyard = ["Ειδήσεις από την Ελλάδα", "Διαβάστε ΕΔΩ περισσότερα", "Πηγή",
                         "Διαβάστε επίσης", "Δείτε όλες τις τελευταίες"]
        recycled_body = [[re.search("(?:(?!" + junk + ").)*", body).group() for junk in body_junkyard]]

        # 2. if there is no space after dot, add one
        add_space_after_dot = r"\.(?=\S)"
        final_body = [re.sub(add_space_after_dot, ". ", body) for body in recycled_body[0]]

        hashed_id = hashlib.md5(item["link"].encode()).hexdigest()

        article = ArticleOfInterest(_id=str(ObjectId(hashed_id[:24])), title=item["title"], date=item["date"],
                                    body=min(final_body, key=len), tags=item["tags"], author=item["author"],
                                    link=item["link"], type=item["type"], scope=item["scope"])
        article.save()
        return item
