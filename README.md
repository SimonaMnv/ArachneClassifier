# Custom Greek article crawler & classifier

## Table of contents

* [General info](#general-info)
* [Technologies](#technologies)
* [Pre-trained model](#technologies)
* [Custom-trained model](#setup)

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
    ├── crawling
    ├── crawling
    └── spiders
and edit the spider.

if you intent to change the structure of the data (fields) then edit the model in:
    
    .
    ├── api 
    └── article_models
    
        
    
* to initiate the scraping run: ```python scrapy crawl newsbomb```, the text is saved in a mongo db (djongo is used) 
* then, index the djongo database with elasticsearch, run: ```python
python manage.py search_index --rebuild```
now that the data is indexed from elastic, go to: 


    ├── nlp_classification
    └── ML_classification
and uncomment the ```export_dataset_df()``` function. This gathers all the **analyzed** data from elastic and exports it to a dataframe.
* The model is trained with SVM and exported.
* Open ```dash/app.py``` to test the custom classification.
