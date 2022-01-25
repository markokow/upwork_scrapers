from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import datetime
import scrapy
import html2text


def get_useragent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1000)
    return user_agent_rotator.get_random_user_agent()


class StackOverFlow(scrapy.Spider):
    name = 'StackOverFlow'

    def start_requests(self):
        with open('stack_urls.txt') as file:
            inputs = file.read().split('\n')
        for input in inputs:
            input = input + 'answertab=votes#tab-top'
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "user-agent": get_useragent()}
            yield scrapy.FormRequest(input, callback=self.post, headers=headers)

    def post(self, response):

        text = html2text.HTML2Text()
        text.ignore_images = True
        text.ignore_links = True
        text.ignore_emphasis = True
        text.body_width = 0
        text.ignore_tables = True

        post = dict()
        post['URL'] = response.url
        try:
            post['Title'] = response.xpath('//h1[@itemprop="name"]//text()').get(default='')
        except:
            post['Title'] = ''
        divs = response.xpath('//div[@class="answercell post-layout--right"]')
        max_answers = 5
        counter = 1
        for div in divs:
            post_body = div.xpath('//div[@class="s-prose js-post-body"]').extract_first()
            post_body = str(post_body)
            post_body = post_body.replace("<div class=\"s-prose js-post-body\" itemprop=\"text\">", " ")
            post_body = post_body[:-6]
            post_body = post_body.strip()
            if counter != max_answers:
                post[f'Best_Answer_{counter}'] = post_body
                counter += 1
            else:
                break
        yield post

from scrapy.cmdline import execute

today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')
execute(f'scrapy runspider stackData.py -o file_{today}.csv -t csv'.split())

