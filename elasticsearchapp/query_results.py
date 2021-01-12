import requests


def get_all_raw_data():
    url = "http://127.0.0.1:9200/articles/_search"
    raw_data = []
    raw_type = []

    payload = "{\r\n  \"track_total_hits\": true, \r\n  \"size\":20000\r\n\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    length = response["hits"]["total"]["value"]
    print("length of data", length)

    for i in range(0, length):
        article_body = response["hits"]["hits"][i]["_source"]["body"] + " " + \
                       response["hits"]["hits"][i]["_source"]["title"] + " " +  \
                       response["hits"]["hits"][i]["_source"]["tags"] + " "
        raw_data.append([article_body])
        raw_type.append(response["hits"]["hits"][i]["_source"]["type"])

    return raw_data, raw_type


def get_all_analyzed_data():
    raw_data, raw_type = get_all_raw_data()
    tokenized_data = []
    tokenized_total = []

    url = "http://127.0.0.1:9200/articles/_analyze"

    for raw_datum in raw_data:
        # escape some characters or tokenization wont work
        raw_datum[0] = raw_datum[0].replace('\n', '').replace('\r', '').replace("\\", '').replace('"', "")\
            .replace("\b", '').replace("\t", '').replace("\f", '')

        payload = "{\r\n  \"analyzer\" : \"greek_analyzer\",\r\n  \"text\" : \"" + raw_datum[0] + "\"\r\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload.encode("utf8"))
        response = response.json()

        tokenized = response["tokens"]
        for token in tokenized:
            tokenized_data.append(token["token"])

        tokenized_total.append(tokenized_data)
        tokenized_data = []

    return tokenized_total, raw_type


def get_specific_analyzed(specific_text):
    tokenized_data = []
    tokenized_total = []

    url = "http://127.0.0.1:9200/articles/_analyze"

    # escape some characters or tokenization wont work
    specific_text = specific_text.replace('\n', '').replace('\r', '').replace("\\", '').replace('"', "")\
        .replace("\b", '').replace("\t", '').replace("\f", '')

    payload = "{\r\n  \"analyzer\" : \"greek_analyzer\",\r\n  \"text\" : \"" + specific_text + "\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload.encode("utf8"))
    response = response.json()

    tokenized = response["tokens"]
    for token in tokenized:
        tokenized_data.append(token["token"])

    tokenized_total.append(tokenized_data)

    return tokenized_total

