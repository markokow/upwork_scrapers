import os
import cv2 
import time
import pyautogui
import numpy as np
from typing import Any

RESIZE_BUTTON = (188, 81)
PIXEL_CLICK = (219, 155)
MAINTAIN_ASPECT = (72, 267)
HORIZONTAL_SIZE = (267, 190)
VERTICAL_SIZE = (270, 230)
PEN_CLICK = (251, 69)
SIZE_CLICK = (633, 80)
SIZE_BIG_CLICK = (675,178)

class Paint_TimeLapse():
    def __init__(self, img_src:str = '', img_size:int = 2, img_dyn_ratio:int = 1) -> None:
        self.img_src = img_src
        self.img_size = img_size
        self.img_dyn_ratio = img_dyn_ratio

    def create_dr(self):
        path = 'output'
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:
        # Create a new directory because it does not exist 
            os.makedirs(path)

    def get_total_unique_colors(self, painted_result: Any):
        total = []
        for idx, _ in enumerate(painted_result):
            if idx == 0:
                total = _.tolist()
            else:
                total = total + _.tolist()
                
        return np.unique(total, axis=0)

    def choose_color(self, red, green, blue):
        pick_custom_color = (960, 101)
        edit_colors_position = (994, 64)
        pyautogui.click(edit_colors_position)
        pyautogui.click((1162, 593))
        pyautogui.hotkey('ctrl', 'a')   
        pyautogui.press(red)
        pyautogui.click((1145, 616))
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press(green)
        pyautogui.click((1155, 632))
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press(blue)
        pyautogui.press('enter')
        pyautogui.click(pick_custom_color)

    def resize_pallete(self, img):
        img_shape = img.shape
        if img_shape[0] > 800:
            raise Exception('Unable to proceed, please set vertical size to be less than 800 pixel.')
        else:
            pyautogui.click(RESIZE_BUTTON)
            pyautogui.click(PIXEL_CLICK)
            pyautogui.click(MAINTAIN_ASPECT)
            pyautogui.click(HORIZONTAL_SIZE)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press(list(str(img_shape[1])))
            pyautogui.click(VERTICAL_SIZE)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press(list(str(img_shape[0])))
            pyautogui.press('enter')

    def check_tools(self):
        pyautogui.click(PEN_CLICK)
        pyautogui.click(SIZE_CLICK)
        pyautogui.click(SIZE_BIG_CLICK)

    def run(self):
        time.sleep(3)
        self.create_dr()
        img = cv2.imread(self.img_src)
        self.resize_pallete(img)
        self.check_tools()
        painted_result = cv2.xphoto.oilPainting(img, self.img_size, self.img_dyn_ratio)
        total_colors = self.get_total_unique_colors(painted_result=painted_result)
        offset = [4, 144]
        time.sleep(1)
        for clr in total_colors: 
            color = clr    
            red = list(str(color[-1]))
            green = list(str(color[1]))
            blue = list(str(color[0]))
            self.choose_color(red, green, blue)
            for i in range(0, len(painted_result)):
                for j in range(0, len(painted_result[0])):     
                    if all(painted_result[i][j] == clr):
                        pyautogui.click((j+1+offset[0],i+1+offset[-1]))

if __name__ == "__main__":
    images = os.listdir("input")
    img_src = f"input/{images[0]}"
    img_size = 2
    img_dyn_ratio = 1
    instance = Paint_TimeLapse(img_src=img_src, img_size=img_size, img_dyn_ratio=img_dyn_ratio)
    instance.run()





