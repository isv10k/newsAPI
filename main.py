import pprint as pp
from news_api import NewsAPI


if __name__ == '__main__':

    categories = ['technology', 'business']

    keywords = ['Trump', 'Joe']

    user_request = 'game of thrones'

    newsapi = NewsAPI(api_key='753fa527aca34ea29bca4b8e67bcba1c')

    # response = newsapi.categories_list_response(categories, country='ru', page_size=10, page=1)

    # response = newsapi.key_words_response(keywords, country='us', page_size=10, page=1)

    response = newsapi.user_request_response(user_request, language='en', page_size=10, page=1)

    pp.pprint(response)
