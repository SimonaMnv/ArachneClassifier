from django.shortcuts import render
from api.models import ArticleOfInterest


def index(request):
    all_articles = ArticleOfInterest.objects.all()
    return render(request, "index.html", {'articles': all_articles})
