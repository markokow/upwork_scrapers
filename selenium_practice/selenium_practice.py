from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 


driver = webdriver.Firefox()

driver.get('https://crs.upd.edu.ph/')
print(driver.title)

search = driver.find_element_by_name('txt_login')
search.send_keys('raapaap')
search = driver.find_element_by_name('pwd_password')
search.send_keys('bryitkids')
search.send_keys(Keys.RETURN)

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'not-paid'))
    )

except:
    driver.quit()


search = driver.find_element_by_xpath("//a[@title='Grades Viewing']")
search.click()

main = driver.find_element_by_class_name('offf')

print(main.text)








