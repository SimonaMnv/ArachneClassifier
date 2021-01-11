from elasticsearchapp.query_results import get_all_analyzed_data
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, svm
from sklearn.metrics import accuracy_score
np.random.seed(500)


def export_dataset_df():
    tokenized_data, raw_type = get_all_analyzed_data()

    total_data = []
    total_types = []

    for data, type in zip(tokenized_data, raw_type):
        total_data.append(data)
        total_types.append(type)

    print(total_data)
    print(total_types)

    df = pd.DataFrame({'article_tokens': total_data, 'crime_type': total_types})
    df.to_csv('../dfs/newsbomb_article.csv', encoding='utf-8-sig', index=False)


# export_dataset_df()
corpus = pd.read_csv('../dfs/newsbomb_article.csv')

train_X, test_X, train_Y, test_Y = model_selection.train_test_split(corpus['article_tokens'],
                                                                    corpus['crime_type'],
                                                                    test_size=0.2)

Encoder = LabelEncoder()
train_Y = Encoder.fit_transform(train_Y)
test_Y = Encoder.fit_transform(test_Y)

# check the given class id
integer_mapping = {l: i for i, l in enumerate(Encoder.classes_)}
print(integer_mapping)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(corpus['article_tokens'])
Train_X_Tfidf = Tfidf_vect.transform(train_X)
Test_X_Tfidf = Tfidf_vect.transform(test_X)

# print(Tfidf_vect.vocabulary_)
# print(Train_X_Tfidf)

# SVM Classifier
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM.fit(Train_X_Tfidf, train_Y)
predictions_SVM = SVM.predict(Test_X_Tfidf)
print("SVM Accuracy Score: ", accuracy_score(predictions_SVM, test_Y)*100)

# test unknown dataset -> not in db
no_label_corpus = pd.read_csv('../dfs/newsbomb_article_predict.csv')
test_unknown = no_label_corpus['article_tokens']

test_unknown_Tfidf = Tfidf_vect.transform(test_unknown)
predictions_SVM = SVM.predict(test_unknown_Tfidf)
print(predictions_SVM)
