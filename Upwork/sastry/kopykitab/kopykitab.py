import pyautogui
import os
import time
import aspose.words as aw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image



class KopyKitab():
    def __init__(self, book_url: str = '', total_pages: int = 1) -> None:
        self.book_url = book_url
        self.total_pages = total_pages
        self.login_url = "https://www.kopykitab.com/index.php?route=account/login"
        self.logout_url = "https://www.kopykitab.com/index.php?route=account/logout"
        self.username = "risinghunks@gmail.com"
        self.password = "Poranki@135"
        self.COORDINATE_TO_FS_1 = (1842, 69)
        self.COORDINATE_TO_FS_2 = (1841, 19)
        self.CENTER_CLICK = (960, 540)
        self.driver = webdriver.Chrome(executable_path=r"chromedriver.exe")

    def create_dr(self):
        path = 'images'
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:
        # Create a new directory because it does not exist 
            os.makedirs(path)


    def run(self):
        self.driver.get(self.login_url)
        time.sleep(1)
        elem = self.driver.find_element_by_name('email')
        elem.clear()
        elem.send_keys(self.username)
        time.sleep(1)
        elem = self.driver.find_element_by_name('password')
        elem.clear()
        elem.send_keys(self.password)
        time.sleep(1)
        elem = self.driver.find_element_by_css_selector('.form_button')
        elem.click()

        self.driver.get(self.book_url)
        time.sleep(3)
        pyautogui.hotkey('f11')
        time.sleep(1)
        pyautogui.click(self.COORDINATE_TO_FS_2)
        pyautogui.click(self.COORDINATE_TO_FS_1)
        time.sleep(2)
        self.create_dr()

        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)

        for i in range(0, 13):
            time.sleep(1)
            self.driver.save_screenshot(f"images/image_{i+1}.png")
            im = Image.open(f"images/image_{i+1}.png")
            width, height = im.size
            
            # Setting the points for cropped image
            left = width * 0.3
            top = 0
            right = width * 0.7
            bottom = height
            
            im1 = im.crop((left, top, right, bottom))
            im1.save(f"images/image_{i+1}.png")
            builder.insert_image(f"images/image_{i+1}.png")
            pyautogui.click(self.CENTER_CLICK)

        doc.save("sample.pdf")

        time.sleep(1)
        self.driver.get(self.logout_url)
        time.sleep(1)
        self.driver.quit()

if __name__ == "__main__":
    book_url = "https://www.kopykitab.com/index.php?route=pdfviewer/view&product_id=30816"
    total_pages = 13
    instance = KopyKitab(book_url=book_url, total_pages=total_pages)
    instance.run()

        








