# ScreenOCR

This was made to copy Python YouTube video text into VSCode because I'm too lazy to type it in.

ocr.py
gets selection from screenshot and saves to file
processes selection via cv2.threshold and saves to file
extracts text with pytesseract
outputs text to terminal and clipboard

TODO
Distorted color displaying screengrab when making selection - RGB displaying as BGR
improve selection rectangle - disappears when mouse not moving
improve on cv2.threshold output
