from instagram_scraper.instagram import InstagramScraper

proxies = {
    'http': 'http://103.215.24.162:5678',
    'https': 'http://88.116.137.130:10801',
}

instagram = InstagramScraper()
instagram.set_proxies(proxies)

account = instagram.get_account('kevin')
account_id = account.get_id()
print(account._id)