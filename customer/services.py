from django.conf import settings
import requests
from datetime import datetime


class SearchNewsService:

    @staticmethod
    def get_news(search_string):
        url = ('https://newsapi.org/v2/everything?'
               'q=' + search_string + '&'
               'sortBy=publishedAt&'
               'from=' + str(datetime.now().date()) + '&'
               'apiKey=' + settings.NEWS_API_KEY)

        response = requests.get(url)
        result = response.json()
        return result

    @staticmethod
    def refresh_news(search_string):
        url = ('https://newsapi.org/v2/everything?'
               'q=' + search_string + '&'
               'sortBy=publishedAt&'
               'from=' + str(datetime.now().date()) + '&'
               'apiKey=' + settings.NEWS_API_KEY)

        response = requests.get(url)
        result = response.json()
        return result

    @staticmethod
    def sort_news(search_string):
        url = ('https://newsapi.org/v2/everything?'
               'q=' + search_string + '&'
               'sortBy=publishedAt&'
               'from=' + str(datetime.now().date()) + '&'
               'apiKey=' + settings.NEWS_API_KEY)

        response = requests.get(url)
        result = response.json()
        return result
