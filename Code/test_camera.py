import cv2

print("Sprawdzanie kamer...")

for i in range(5):
    cap = cv2.VideoCapture(i)

    if cap.isOpened():
        ret, frame = cap.read()

        if ret:
            print(f"Kamera {i}: DZIALA")
        else:
            print(f"Kamera {i}: otwarta, ale brak obrazu")

        cap.release()
    else:
        print(f"Kamera {i}: brak")

print("Gotowe")