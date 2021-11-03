from facebook_scraper import get_profile
data = get_profile("zuck") # Or get_profile("zuck", cookies="cookies.txt")

print(data)