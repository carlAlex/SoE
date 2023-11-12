import numpy as np
import win32gui, win32ui, win32con
import mss
import cv2 as cv
from threading import Thread, Lock
import pyautogui

class Detection:
    '''
    This class is used to detect a needle image in a haystack image.
    
    The needle image is loaded from a file and then the find_needle() method
    is called to check if the current screenshot contains the needle image.

    The find_needle() method returns True if the needle image is found, and
    False if it is not found.

    The needle_point property contains the x, y coordinates of the top-left
    corner of the needle image in the haystack image. This can be used to
    move the mouse to the center of the needle image, for example.

    The update() method is used to update the haystack image. This should be
    called before find_needle() is called.
    '''
    # constants
    IMAGE_MATCH_THRESHOLD = 0.72
    FIND_THIS_IMAGE = 'SoE\\img\\food_cheese.png'

    # threading properties
    lock = None
    rectangles = []
    needle_point = ()
    # properties
    screenshot = None

    def __init__(self, model_file_path: str=""):
        # create a thread lock object
        self.lock = Lock()
        self.needle_image = cv.imread(self.FIND_THIS_IMAGE, cv.IMREAD_UNCHANGED)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def find_needle(self):
        """
        Check if the current screenshot contains the needle_image.
        """
        img = cv.imread(self.FIND_THIS_IMAGE)
        scrSh = np.array(self.screenshot)
        # cv.imshow('Shot', scrSh)
        result = cv.matchTemplate(scrSh, img, cv.TM_CCOEFF_NORMED)
        # get the best match postition
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # print max_val which is the confidence of a match
        print('Confidence of match: {}'.format(max_val))
        
        if max_val >= self.IMAGE_MATCH_THRESHOLD:
            # print('max_val > threshold')
            print('Image found at {}'.format(max_loc))
            self.needle_point = max_loc
            return True
        print('Image not found.')
        return False

class WindowCapture:
    '''
    This class is used to capture a window or part of a window using the
    win32gui, win32ui, and win32con libraries, and then to provide an
    interface to grab screenshots of that window.

    Alternatively if mss is installed (https://python-mss.readthedocs.io/en/latest/)
    then mss can be used instead, which is a lot faster but Windows only.

    list_window_names() can be used to get the names of other running windows
    on the computer that can be used with this class.

    get_screenshot() returns a screenshot of the window as a numpy array.

    get_mss_screenshot() returns a screenshot of the window as a numpy array
    using mss. It captures the screen as is, so make sure the window is not
    obscured by anything.
    '''
    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_mss_screenshot(self):
        monitor = {"top": self.offset_y, "left": self.offset_x, "width": self.w, "height": self.h}
        sct = mss.mss()
        screenshot = sct.grab(monitor)
        # convert the screenshot to a numpy array
        screenshot = np.array(screenshot)

        return screenshot

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        # img = np.fromstring(signedIntsArray, dtype='uint8')
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
        

# NOTE: Denne koden kan 'uncommentes' for å finne navnet på vinduet du ønsker å ta screenshot av.
# def list_window_names():
#         def winEnumHandler(hwnd, ctx):
#             if win32gui.IsWindowVisible(hwnd):
#                 print(hex(hwnd), win32gui.GetWindowText(hwnd))
#         win32gui.EnumWindows(winEnumHandler, None)
# list_window_names()

# Bruk funksjonen over til å finne 100% navnet på vinduet.. Som du ser MÅ navnen på character
# være med. Men det finner du med å kommentere bort alt dette og bare kjøre koden over.

wc = WindowCapture('Souls Of Elysium - BRUKERNAVN')

# NOTE: Begge disse fungerer for å ta screenshot av vinduet.

# Uncomment denne for å ta screenshot med win32gui
# image = wc.get_screenshot()
# cv.imwrite('SoE\img\get_screenshot.png', image)

# Uncomment denne for å ta screenshot med mss (spill vinduet må ikke være bak noe annet)
# image = wc.get_mss_screenshot()
# cv.imwrite('SoE\img\get_mss_screenshot.png', image)

det = Detection()
det.update(wc.get_screenshot())
if det.find_needle():
    print('Found!')
    game_win_x = wc.offset_x
    game_win_y = wc.offset_y
    # move mouse with pyautogui to the center of the needle image
    pyautogui.moveTo(game_win_x + det.needle_point[0], game_win_y + det.needle_point[1])
else:
    print('Not found!')