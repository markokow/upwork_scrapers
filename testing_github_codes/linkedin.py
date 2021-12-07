from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Firefox()

email = "lopper.apaap@gmail.com"
password = "bryitkids"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)

person.scrape()