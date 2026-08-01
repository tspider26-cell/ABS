import cv2
import time

from camera import Camera
from config import *

camera = Camera(CAMERA_INDEX)
last_time = time.time()

while True:
    success, frame = camera.read()
    if not success:
        print("Nie udało się odczytać obrazu z kamery.")
        break

    now = time.time()
    fps = 1 / max(now - last_time, 1e-6)
    last_time = now

    if SHOW_FPS:
        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
