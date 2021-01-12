from django_elasticsearch_dsl import Index, fields
from django_elasticsearch_dsl.documents import Document
from api.models.article_model import ArticleOfInterest
from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl.registries import registry
from elasticsearchapp.custom_analyzers import greek_analyzer

connections.create_connection()

article_index = Index('articles')

article_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@registry.register_document
@article_index.document
class ArticleDocument(Document):
    title = fields.TextField(analyzer=greek_analyzer)
    date = fields.DateField()
    body = fields.TextField(analyzer=greek_analyzer)
    tags = fields.TextField(analyzer=greek_analyzer)
    author = fields.TextField()
    link = fields.TextField()
    type = fields.TextField()
    scope = fields.TextField()

    class Django:
        model = ArticleOfInterest
