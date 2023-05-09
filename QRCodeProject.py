import cv2
import time
import numpy as np
from pyzbar.pyzbar import decode

# Authorized ids
with open('IDs.txt') as f:
	idsList = f.read().splitlines()

# Active camera
cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 480)

while True:
    success, image = cap.read()

    for barcode in decode(image):
        id = barcode.data.decode('utf-8')
        print(id)

        # Check authorized ids
        if id in idsList:
            output = 'Authorized'
            color = (0, 255, 0)
        else:
            output = 'Un-Authorized'
            color = (0, 0, 255)

        # Points for QRCode
        ptsQR = np.array([barcode.polygon], np.int32)
        ptsQR = ptsQR.reshape((-1, 1, 2))
        cv2.polylines(image, [ptsQR], True, color, 5)

        # Points for put text
        pts = barcode.rect
        cv2.putText(image, output, (pts[0], pts[1]), cv2.FONT_HERSHEY_COMPLEX,
                    0.9, color, 2)

    # Get current time
    current_time = str(time.ctime())
    cv2.putText(image, current_time, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

    # Show results
    cv2.imshow('Live', image)

    # To exit from live, press Esc key
    if cv2.waitKey(1) & 0xFF == 27: # 27 is the Esc Key
        break

# release camera and close windows
cap.release()
cv2.destroyAllWindows()