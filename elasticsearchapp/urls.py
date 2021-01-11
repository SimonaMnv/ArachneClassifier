from elasticsearchapp import viewsets
from rest_framework.routers import SimpleRouter

app_name = 'elasticsearchapp'

router = SimpleRouter()
router.register(
    prefix=r'',
    basename='elasticsearchapp',
    viewset=viewsets.ArticleDocumentView
)
urlpatterns = router.urls
