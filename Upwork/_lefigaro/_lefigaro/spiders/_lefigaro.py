from urllib import parse
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import headers
from scrapy.selector import Selector
import time
import json

class LefiGaro(scrapy.Spider):

    name = '_lefigaro'
  
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
    
    _base_url = 'https://api-graphql.lefigaro.fr/graphql?id=widget-comments_commentsQuery2_31d9f1fd61a3568936b76800aef3aade1b9002eee01930e2b9c499ceca28192e&variables={"id":"bGVmaWdhcm8uZnJfX2I0NjZhMTE2LTFjNzktMTFlYy04ZmYwLWEwMzY5ZjkxZjMwNF9fQXJ0aWNsZQ==","page":'
    _child_url = 'https://api-graphql.lefigaro.fr/graphql?id=widget-comments_commentRepliesQuery2_f6f03af22e6093fb8d5a69caf102e33ae439b8587d763475a300e041d7985d10&variables={"id":"'

    def start_requests(self):

        for _page in range(1, 17):

            _url =  self._base_url + str(_page) + '}'

            try:
                yield scrapy.Request(url = _url, headers = self.headers, callback=self.parse)
            except:
                pass


    def parse(self, response, **kwargs):
        
        _data = json.loads(response.text)

        _comments = _data['data']['comments']

        for _comment in _comments:

            _features = {
                'UniqueID': _comment['id'].strip(),
                'Contributor': _comment['author']['username'].strip(),
                'Premium User': _comment['author']['isPremium'],
                'Date': _comment['createdAt'].split('T')[0].strip(),
                'Time': _comment['createdAt'].split('T')[-1].strip(),
                'Comment': _comment['text'].strip(),
                'Child': 1 if self._child_url in str(response.url) else 0,
            }

            yield _features

            if self._child_url in response.url:
                _url_child = self._child_url + _features['UniqueID'] + '}'

                try:
                    yield scrapy.Request(url = _url_child, headers = self.headers, callback=self.parse)
                except:
                    pass
            else:
                continue
        




