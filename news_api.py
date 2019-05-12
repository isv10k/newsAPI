import requests
from news_auth import NewsApiAuth
from concurrent.futures import ThreadPoolExecutor, as_completed


def make_params(country, language, page_size, page):
    """Returns dict with parameters"""
    params = dict()

    if country:
        params['country'] = country
    if language:
        params['language'] = language
    if page_size:
        params['pageSize'] = page_size
    if page:
        params['page'] = page

    return params


def custom_request(parameter_value, parameter_name, payload, authorization, endpoint='top-headlines'):
    """Returns dict with parameter_value as a key and a response from request as a value."""
    url = 'https://newsapi.org/v2/' + endpoint

    # Adding parameter to query
    payload[parameter_name] = parameter_value

    response = requests.get(url, params=payload, auth=authorization)

    parameter_news = dict()

    parameter_news[parameter_value] = response.json()

    return parameter_news


def threaded_request_execution(parameter_value_list, parameter_name, payload, auth):
    """Executes several requests using threads"""
    with ThreadPoolExecutor() as pool:
        futures = [
            pool.submit(custom_request, parameter_value, parameter_name, payload, auth)
            for parameter_value in parameter_value_list
        ]
        result = {}
        for future in as_completed(futures):
            news_by_parameter = future.result()
            # Merge with previous result
            result = {**result, **news_by_parameter}

    return result


class NewsAPI:

    def __init__(self, api_key: str):
        self.auth = NewsApiAuth(api_key=api_key)

    def categories_list_response(self, categories_list=[], country='', language='', page_size='', page=''):
        """Returns response for search by categories list"""

        payload = make_params(country, language, page_size, page)

        parameter_name = 'category'

        response = threaded_request_execution(categories_list, parameter_name, payload, self.auth)

        return response

    def key_words_response(self, keywords_list=[], country='', language='', page_size='', page=''):
        """Return response for search by key worlds"""

        payload = make_params(country, language, page_size, page)

        parameter_name = 'q'

        response = threaded_request_execution(keywords_list, parameter_name, payload, self.auth)

        return response

    def user_request_response(self, user_request='', country='', language='', page_size='', page=''):
        """Return response for user request"""

        payload = make_params(country, language, page_size, page)

        parameter_name = 'q'
        # Changed enpoint for more possible results
        response = custom_request(user_request, parameter_name, payload, self.auth, endpoint='everything')

        return response

