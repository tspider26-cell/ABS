
import cv2

class CameraManager:
    def available_cameras(self, max_index=5):
        cameras=[]
        for i in range(max_index):
            cap=cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras
