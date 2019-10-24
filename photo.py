import cv2
import time
camera = cv2.VideoCapture(0)

while(True):
    ret, img = camera.read()
    
    cv2.imshow('image', img)
    cv2.imwrite('0001.jpg',img)

    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
        cap.release()
        cv2.destroyAllWindows()
        break
    