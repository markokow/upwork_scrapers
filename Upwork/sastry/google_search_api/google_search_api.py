from re import S
from selenium import webdriver
import time
import pandas as pd
  
# Main Function
if __name__ == '__main__':

    df = pd.read_csv("QData.csv", encoding='latin-1')
    search = df["item"] + " quorum"

    print(search)

  
    # options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # options.add_argument('--log-level=3')

    # df = pd.read_csv("QData.csv")

    # print(df)





  
    # Provide the path of chromedriver present on your system.
    # driver = webdriver.Chrome(executable_path="chromedriver",
    #                           chrome_options=options)
    # driver.set_window_size(1920,1080)
  
    # Send a get request to the url
    # driver.get('https://www.google.com/search?hl=en&gl=us&tbm=shop&psb=1&q=11525-4+quorum')
    # time.sleep(60)
    # driver.quit()
    print("Done")