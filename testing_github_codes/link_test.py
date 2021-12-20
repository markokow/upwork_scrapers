from linkedin_scraper import Company
from selenium import webdriver
driver = webdriver.Firefox()
company = Company("https://ca.linkedin.com/company/google", driver = driver)

print(company)