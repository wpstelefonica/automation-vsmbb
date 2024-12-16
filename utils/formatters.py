import json


def format_json_response(response: str):
    data = json.loads(response)

    raw_query = data["query"]

    formatted_query = raw_query.replace("\n", " ").replace("'", '"')
    normalized_query = " ".join(formatted_query.split())
    return normalized_query


def format_query_str(string: str):
    formatted_query = string.replace("\n", " ")
    normalized_query = " ".join(formatted_query.split())
    return normalized_query
