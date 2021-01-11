from djongo import models
# from article_analysis import CrimeAnalysis


class ArticleOfInterest(models.Model):
    _id = models.ObjectIdField()
    title = models.TextField(null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    tags = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255, unique=False)
    link = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    scope = models.TextField(null=True, blank=True)
    # crime_analysis = models.ForeignKey(CrimeAnalysis, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'db_article'
