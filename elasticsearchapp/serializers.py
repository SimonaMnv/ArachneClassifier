from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from elasticsearchapp.documents import ArticleDocument


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument

        fields = (
            'title',
            'date',
            'body',
            'tags',
            'author',
            'link',
            'type',
            'scope',
        )
