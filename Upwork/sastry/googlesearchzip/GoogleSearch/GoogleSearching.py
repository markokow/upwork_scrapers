import datetime
import re
import requests
import scrapy
from scrapy.http import HtmlResponse
import pandas as pd


class GoogleSearch(scrapy.Spider):
    name = 'GoogleSearch'
    mainAnswer = 11
    postList = []

    def start_requests(self):
        with open('input.txt') as file:
            inputs = file.read().split('\n')
            for input in inputs:
                header = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
                link = f'https://www.google.com/search?q={input}'
                count = 1
                yield scrapy.FormRequest(url=link, callback=self.parse, headers=header, meta={'count': count})
                # break

    def parse(self, response, **kwargs):
        ress = requests.session()
        count = response.meta['count']
        f = open('1.html', 'wb')
        f.write(response.body)
        f.close()
        divs = response.xpath('//div[@jsname="Cpkphb"]')
        anss = re.findall('role\\\\x3d\\\\x22heading(.*?)\\\\x22\\\\x3e\\\\x3ca', response.text)
        question = []
        questionNumber = 0
        post = dict()
        while divs != []:
            Ansnum = 0
            for div in divs:
                try:
                    ques = div.xpath('.//div[contains(text(),"Search for: ")]/a/text()').get()
                except:
                    ques = div
                try:
                    ans = anss[Ansnum]
                except:
                    ans = ''
                if ans != '':
                    ans1 = f'<{ans}</div>'.replace("\\", '').replace('x3dx22', '="').replace('x22', '"').replace('x3c',
                                                                                                                 '<').replace(
                        'x3e', '>').replace('</</div>', '</div>').split('<')
                    del ans1[0]
                    del ans1[0]
                    ans1 = '<'.join(ans1)
                    ans = '<' + ans1.split('</span></span>')[0] + '</span></span>'
                    if self.mainAnswer > count:
                        if ques in str(question):
                            pass
                        else:
                            question.append(ques)
                            post[f'question_{count}'] = ques
                            post[f'answert_{count}'] = ans
                            count += 1
                            Ansnum += 1
                    else:
                        divs = []
            if divs != []:
                header = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
                link = f'https://www.google.com/search?q={question[questionNumber]}'
                res = ress.get(url=link, headers=header)
                res = HtmlResponse(url=link, body=res.content)
                questionNumber += 1
                divs = res.xpath('//div[@jsname="Cpkphb"]')
                anss = re.findall('role\\\\x3d\\\\x22heading(.*?)\\\\x22\\\\x3e\\\\x3ca', res.text)
                del anss[0]
            else:
                divs = []
        else:
            self.postList.append(post)
            pass

    def close(spider, reason):
        today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')

        df = pd.DataFrame(GoogleSearch.postList)
        df.to_csv(f'GoogleResult_{today}.csv')


from scrapy.cmdline import execute

execute(f'scrapy runspider GoogleSearching.py'.split())
