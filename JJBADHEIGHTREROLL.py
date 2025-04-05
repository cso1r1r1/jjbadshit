# An unoptimized script but works,
# todo: set tesseract oct path at line 17 (dont remove "r"), set the debugging image location at line 96 (dont remove the "r")
# paste this into cmd
# pip install pytesseract
# pip install keyboard
# pip install pyautogui
# pip install mss
# pip install numpy
# launch the app and use the coordinate selector to select your hp value, dont include decimals. screenshot the coordinates then paste it into the program
# min value and max value are the hp thresholds, i recommend setting them to 159-200 (it searches between those values)
# press start then tab out the program quickly since it will start pressing 3 and left click automaticly if the value is not right. (selects RerollCharacter and presses Left click if you dont have the set hp)
# when you get the right value, it will stop the program and close it automaticly.




import tkinter as tk
import threading
import time
import mss
import numpy as np
import pytesseract
import keyboard
import pyautogui
import cv2
from PIL import Image
import re

# Set Tesseract OCR path
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = tesseract_path

class AutoClickerBot:
    def __init__(self, root):
        self.root = root
        self.root.title("funny jjbad height bot by csogi")
        self.running = False
        
        self.start_button = tk.Button(root, text="Start", command=self.start_bot, width=20, height=2)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_bot, width=20, height=2, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Status: Idle", fg="blue")
        self.status_label.pack(pady=10)

        self.label_x = tk.Label(root, text="Left X:")
        self.label_x.pack()
        self.entry_x = tk.Entry(root)
        self.entry_x.pack()

        self.label_y = tk.Label(root, text="Top Y:")
        self.label_y.pack()
        self.entry_y = tk.Entry(root)
        self.entry_y.pack()

        self.label_width = tk.Label(root, text="Width:")
        self.label_width.pack()
        self.entry_width = tk.Entry(root)
        self.entry_width.pack()

        self.label_height = tk.Label(root, text="Height:")
        self.label_height.pack()
        self.entry_height = tk.Entry(root)
        self.entry_height.pack()

        self.label_min = tk.Label(root, text="Minimum Value:")
        self.label_min.pack()
        self.entry_min = tk.Entry(root)
        self.entry_min.pack()

        self.label_max = tk.Label(root, text="Maximum Value:")
        self.label_max.pack()
        self.entry_max = tk.Entry(root)
        self.entry_max.pack()

        self.value_detected_label = tk.Label(root, text="", fg="green")
        self.value_detected_label.pack(pady=10)

    def start_bot(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running", fg="green")
        
        threading.Thread(target=self.run_bot, daemon=True).start()

    def stop_bot(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg="red")
    
    def capture_screen(self, region):
        with mss.mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            return img
    
    def preprocess_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        return Image.fromarray(thresh)

    def detect_text(self, image):
        processed_image = self.preprocess_image(image)
        processed_image.save(r"C:\Users\asd\Desktop\debug_capture.png")
        text = pytesseract.image_to_string(processed_image, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        print(f"OCR raw output: {text}")
        return text
    
    def extract_numeric_value(self, text):
        match = re.search(r'\d+', text)
        if match:
            value = int(match.group())
            print(f"Extracted numeric value: {value}")
            return value
        print("No numeric value found.")
        return None
    
    def run_bot(self):
        consecutive_checks = 0
        previous_value = None
        
        time.sleep(0.2)

        while self.running:
            try:
                left = int(self.entry_x.get())
                top = int(self.entry_y.get())
                width = int(self.entry_width.get())
                height = int(self.entry_height.get())
                min_value = int(self.entry_min.get())
                max_value = int(self.entry_max.get())
            except ValueError:
                self.status_label.config(text="Status: Invalid coordinates or range values", fg="red")
                return
            
            region = {'left': left, 'top': top, 'width': width, 'height': height}
            
            screenshot = self.capture_screen(region)
            detected_text = self.detect_text(screenshot)
            detected_value = self.extract_numeric_value(detected_text)
            
            if detected_value and min_value <= detected_value <= max_value:
                if previous_value is None or detected_value == previous_value:
                    consecutive_checks += 1
                else:
                    consecutive_checks = 0
                
                if consecutive_checks >= 4:
                    print(f"Detected value: {detected_value}")
                    self.status_label.config(text=f"Status: Value {detected_value} detected, stopping", fg="blue")
                    
                    self.value_detected_label.config(text=f"Value {detected_value} detected. Auto-stopping.")
                    
                    keyboard.press_and_release("3")
                    pyautogui.click()
                    
                    time.sleep(2)
                    
                    self.running = False
                    self.root.quit()
                    break
                else:
                    self.status_label.config(text="Status: Checking consistency", fg="orange")
            else:
                keyboard.press_and_release("3")
                pyautogui.click()
                self.status_label.config(text="Status: Adjusting (outside range)", fg="orange")
            
            previous_value = detected_value
            time.sleep(0.3)

if __name__ == "__main__":
    root = tk.Tk()
    bot = AutoClickerBot(root)
    root.mainloop()

