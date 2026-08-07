import cv2

cam_id = 0

cap = cv2.VideoCapture(cam_id)

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow("ABS Camera Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()