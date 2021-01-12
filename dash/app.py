import pickle
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from elasticsearchapp.query_results import get_specific_analyzed

# Define app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)
server = app.server

# Load SVM Model
filename = '../nlp_classification/svm_classifier.sav'
loaded_model = pickle.load(open(filename, 'rb'))
# original dictionary (for the vectorization)
corpus = pd.read_csv('../dfs/newsbomb_articles_train.csv')

controls = dbc.Card([
    dbc.Spinner(
        [
            dbc.Button("Classify Crime", id="button-run", block=True),
            html.Div(id="time-taken"),
        ]
    ),
],
    body=False,
    style={"height": "40px"},
)

# Define Layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row([
        html.H1("Greek Text Classification")], align='center'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    width=3,
                    children=[
                        dbc.Card(
                            body=True,
                            children=[
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Classified Type", color="secondary"),
                                        dcc.Textarea(
                                            id="classified-content",
                                            style={
                                                "width": "100%",
                                                "height": "calc(20vh - 275px)",
                                            },
                                        ),
                                    ]
                                )
                            ],
                        ),
                    ],
                ),
                dbc.Col(
                    width=7,
                    children=[
                        dbc.Card(
                            body=True,
                            children=[
                                controls,
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Original Greek Article (Paste here)", color="secondary"),
                                        dcc.Textarea(
                                            id="original-text",
                                            required=True,
                                            lang='gr',
                                            style={"width": "100%", "height": "70vh"},
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                ),
            ]
        ),
    ],
)


@app.callback(
    (
        Output("classified-content", "value")
    ),
    [
        Input("button-run", "n_clicks")
    ],
    [
        State("original-text", "value")
    ]
)
def summarize(n_clicks, original_text):
    if original_text is None or original_text == "":
        return ''

    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(corpus['article_tokens'])

    original_text.replace('\n', '').replace('\r', '').replace("\\", '').replace('"', "") \
        .replace("\b", '').replace("\t", '').replace("\f", '')

    # classify the user's input
    tokenized_original_text = get_specific_analyzed(original_text)
    test_unknown = [', '.join('"{0}"'.format(w) for w in tokenized_original_text)]
    test_unknown_Tfidf = Tfidf_vect.transform(test_unknown)
    classification_SVM = loaded_model.predict(test_unknown_Tfidf)

    results = {
        'ΑΛΛΟ ΕΓΚΛΗΜΑ': 0, 'ΔΟΛΟΦΟΝΙΑ': 1, 'ΛΗΣΤΕΙΑ/ΚΛΟΠΗ': 2, 'ΝΑΡΚΩΤΙΚΑ': 3,
        'ΣΕΞΟΥΑΛΙΚΟ ΕΓΚΛΗΜΑ': 4, 'ΤΡΟΜΟΚΡΑΤΙΚΗ ΕΠΙΘΕΣΗ': 5
    }
    classification_result = ""

    for crime, label in results.items():
        if classification_SVM == label:
            classification_result = crime

    return classification_result


if __name__ == "__main__":
    app.run_server(debug=True)
