# Custom Greek article crawler & classifier

## Table of contents

* [General info](#general-info)
* [Technologies](#technologies)
* [Pre-trained model](#technologies)
* [Custom training](#setup)

## General info

ArachneClassifier is a project for crawling, indexing, analyzing and classifying Greek articles. 
Currently it crawls pages from a Greek news site, specifically, crime articles and classifies them based on the crime type. Crawling and classification is customizable. 

## Technologies

| |Version|
| ------------- |:-------------:|
| Python         |3.8  |
| Elasticsearch | 7.10.1|
| Dash | 1.18.1|
| Scrapy| 2.4.1|
| Spacy |2.3.5 |
| Django| 3.1.4|
| Djongo| 1.3.3|

### Requirements

install frozen-requirements from the main folder and requirements from the dash subfolder

## Pre-trained model
To use the pre-trained model that classifies Greek article crime types install and set up elasticsearch and  run: 
```python
python manage.py search_index --rebuild
```
to create the elasticsearch analyzers with which we will preprocess each article. Each article is tokenized, lowercased, stemmed and stop words are removed from it. 

Use ``dash/app.py`` to open up a flask api where you paste a crime article and it classifies the type.

## Custom-trained model
To crawl different pages go to:
    .
    ├── build                   # Compiled files (alternatively `dist`)
    ├── docs                    # Documentation files (alternatively `doc`)
    ├── src                     # Source files (alternatively `lib` or `app`)
    ├── test                    # Automated tests (alternatively `spec` or `tests`)
    ├── tools                   # Tools and utilities
    ├── LICENSE
    └── README.md

