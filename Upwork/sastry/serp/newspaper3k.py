from newspaper import Article, bui

url = 'https://balconygardenweb.com/growing-chives-in-pots-and-care/'

article = Article(url)
article.download()

article.parse()

# print(article.text)

articles = 