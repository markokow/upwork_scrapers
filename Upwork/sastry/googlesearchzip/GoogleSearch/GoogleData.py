import datetime
import re
import time

import requests
import scrapy
from scrapy.http import HtmlResponse
import pandas as pd
from numpy import random

class GoogleSearch(scrapy.Spider):
    name = 'GoogleSearch'
    mainAnswer = 26
    postList = []
    currentPost = []
    part: int = 1
    idx: int = 0
    limit: int = 20
    today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')


    def start_requests(self):
        with open('input.txt') as file:
            inputs = file.read().split('\n')
            count = 1
            for input in inputs:
                print(input)
                link = f'https://www.google.com/search?q={input}'
                sleeptime = random.uniform(5, 10)
                time.sleep(sleeptime)
                header = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-language": "en-US,en;q=0.9", "cache-control": "max-age=0", "sec-ch-ua-mobile": "?0", "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}

                yield scrapy.FormRequest(url=link, callback=self.parse, headers=header, meta={'count': count, 'input': input})

    def parse(self, response, **kwargs):  # sourcery skip: low-code-quality
        ress = requests.session()
        count = response.meta['count']
        divs = response.xpath('//div[@jsname="Cpkphb"]')
        anss = re.findall('role\\\\x3d\\\\x22heading(.*?)\\\\x22\\\\x3e\\\\x3ca', response.text)
        del anss[0]
        question = []
        questionNumber = 0
        post = {'keyword': response.meta['input']}
        while divs != []:
            Ansnum = 0
            for div in divs:
                try:
                    ques = div.xpath('.//div[contains(text(),"Search for: ")]/a/text()').get()
                except Exception:
                    ques = div
                try:
                    ans = anss[Ansnum]
                except Exception:
                    ans = ''
                if ans != '':
                    ans1 = f'<{ans}</div>'.replace("\\", '').replace('x3dx22', '="').replace('x22', '"').replace('x3c',
                                                                                                                 '<').replace(
                        'x3e', '>').replace('</</div>', '</div>').split('<')
                    del ans1[0]
                    del ans1[0]
                    ans1 = '<'.join(ans1)
                    ans = '<' + ans1.split('</span></span>')[0]
                    if '</div></div></div>' in ans:
                        ans = ans.split('</div></div></div>')[0]
                    ans = f'<div>{ans}</div>'
                    if self.mainAnswer > count:
                        if ques not in str(question):
                            tag_divs = re.findall("<.*?>", ans)
                            text_divs = re.findall('>(.*?)<', ans)
                            adding_ = ans.split('>')[-1]
                            divs.append(adding_)
                            createtext = ''
                            for i in range(len(text_divs)):
                                tag = tag_divs[i]
                                text = text_divs[i]
                                if '})' in text:
                                    text = ''
                                if '<b>' in tag or '<li' in tag or '<ul' in tag or '<p' in tag or '</b' in tag or '</li' in tag or '</ul' in tag or '</p' in tag:
                                    if '<ul' in tag: tag = '<ul>'
                                    if '<li' in tag: tag = '<li>'
                                    if '<p' in tag: tag = '<p>'
                                    if '<b' in tag: tag = '<b>'
                                    if '</ul' in tag: tag = '</ul>'
                                    if '</li' in tag: tag = '</li>'
                                    if '</p' in tag: tag = '</p>'
                                    if '</b' in tag: tag = '</b>'
                                    if '/' in tag:
                                        createtext += f'{text}{tag}' if text not in createtext else tag
                                    else:
                                        createtext += f'{tag}{text}'
                                elif text != '':
                                    createtext += text

                            question.append(ques)
                            post[f'question_{count}'] = ques
                            post[f'answer_{count}'] = createtext.replace('x26#39;',"\'").replace("x26lt;x26gt;","").replace("x26quot;","\"")
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
                sleeptime = random.uniform(5, 10)
                time.sleep(sleeptime)
                res = ress.get(url=link, headers=header)
                res = HtmlResponse(url=link, body=res.content)
                # time.sleep(5)
                questionNumber += 1
                divs = res.xpath('//div[@jsname="Cpkphb"]')
                anss = re.findall('role\\\\x3d\\\\x22heading(.*?)\\\\x22\\\\x3e\\\\x3ca', res.text)
                del anss[0]
            else:
                divs = []

        if 'answer_1' in post.keys():
            self.postList.append(post)
            self.currentPost.append(post)
            self.idx += 1
        
        if ((self.idx) % self.limit) == 0:
            df = pd.DataFrame(self.currentPost)
            df.to_csv(f'{self.today}_part{self.part}.csv', encoding='utf-8-sig')
            self.currentPost = []
            self.part += 1

    def close(self, reason):
        if ((self.idx) % self.limit) != 0:
            df = pd.DataFrame(self.currentPost)
            df.to_csv(f'{self.today}_part{self.part}.csv', encoding='utf-8-sig')
        
from scrapy.cmdline import execute

execute(f'scrapy runspider GoogleData.py'.split())