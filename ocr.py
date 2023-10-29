""" ocr.py
    gets selection from screenshot and saves to file
    processes selection via cv2.threshold and saves to file
    extracts text with pytesseract
    output text to terminal and clipboard
    TODO
    improve selection rectangle
"""
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab
import pytesseract as pyt
import clipboard

# Create a named window
cv2.namedWindow("image")

# Initialise globals
pyt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
start_pos = None
end_pos = None
finished = False
last_rect = None
selected_area = None
screenshot = ImageGrab.grab()
# Create a blank image with transparent background
# overlay = Image.new("RGBA", screenshot.size, (0, 0, 0, 0))
overlay = np.array(screenshot)


def mouse_callback(event, x, y, flags, param):
    global start_pos, end_pos, finished, last_rect, overlay, selected_area

    def minmax(num1, num2):
        smallest = min(num1, num2)
        largest = max(num1, num2)
        return smallest, largest

    def get_area(start_pos, end_pos):
        start_x, end_x = minmax(start_pos[0], end_pos[0])
        start_y, end_y = minmax(start_pos[1], end_pos[1])
        return (start_x, start_y, end_x, end_y)

    if event == cv2.EVENT_LBUTTONDOWN:
        # Initalise positions on mousedown
        start_pos = (x, y)
        end_pos = (x, y)

    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # Update end_pos on mouse drag
        end_pos = (x, y)

    if start_pos and end_pos and start_pos != end_pos:
        # Create a new overlay to draw updated rectangle
        overlay = np.array(screenshot)
        sx, sy, ex, ey = get_area(start_pos, end_pos)
        last_rect = (sx, sy), (ex, ey)
        cv2.rectangle(overlay, (last_rect[0]), (last_rect[1]), (0, 255, 0), 2)
        cv2.imshow("image", overlay)

    if event == cv2.EVENT_LBUTTONUP:
        # On mouseup crop and save selected_area and flag finished
        selected_area = screenshot.crop(get_area(start_pos, end_pos))
        selected_area.save("selected_area.png", "png")
        finished = True


def main():
    global last_rect, overlay, selected_area
    # Use mouse_callback function for namedWindow
    cv2.setMouseCallback("image", mouse_callback)

    while True:
        if last_rect:
            # Redraw the last rectangle for no mouse movement
            cv2.rectangle(overlay, (last_rect[0]), (last_rect[1]), (0, 255, 0), 2)
        # Show the screenshot in the named window
        cv2.imshow("image", np.array(screenshot))
        # Check for key press (wait 1ms) - avoids python kernel crashing
        key = cv2.waitKey(1) & 0xFF
        if finished or key == ord("q"):
            # Quit loop
            break
    # Close all open windows
    cv2.destroyAllWindows()

    selection = cv2.imread("selected_area.png")
    grey_img = cv2.cvtColor(selection, cv2.COLOR_BGR2GRAY)

    # cv2.threshold(grayscale_image, threshold_value, value_assigned, thresholding_type)
    # applying Otsu thresholding passed as an extra flag in binary thresholding

    # blur_img = cv2.GaussianBlur(grey_img,(5,5),0)
    thresh, ocr_img = cv2.threshold(
        grey_img, 40, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    # cv2.imshow('Otsu Threshold', adjusted)
    cv2.imwrite("selected_area_B&W.png", ocr_img)
    cv2.waitKey(1) & 0xFF
    cv2.destroyAllWindows()

    text = pyt.image_to_string(ocr_img)
    clipboard.copy(text)
    print(f"╔══════════════╗")
    print(f"║ OUTPUT  TEXT ║ Threshold used: {thresh}")
    print(f"╚══════════════╝")
    print(text)
    print(f"╔════════════════╗")
    print(f"║ PROGRAM  ENDED ║")
    print(f"╚════════════════╝")


if __name__ == "__main__":
    main()
