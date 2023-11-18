import dxcam
import cv2
from PIL import Image
import time

camera = dxcam.create()  # returns a DXCamera instance on primary monitor

# frame = camera.grab()

# left, top = (1920 - 640) // 2, (1080 - 640) // 2
# right, bottom = left + 640, top + 640
left, top = 1280, 31
right, bottom = 2558, 1398
region = (left, top, right, bottom)

# frame = camera.grab(region=region)  # numpy.ndarray of size (640x640x3) -> (HXWXC)

start_time, fps = time.perf_counter(), 0
start = time.perf_counter()
while fps < 1000:
    frame = camera.grab(region=region)
    if frame is not None:  # New frame
        fps += 1
end_time = time.perf_counter() - start_time
print(f"FPS: {fps/end_time}")

# Display the image
Image.fromarray(frame).show()