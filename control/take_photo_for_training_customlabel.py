#Camera video capture, while running this code, it show the Camera video, at the same time it will also capturing the video, if you press q button it will stop capturing and save the file call handsomeboy.avi in your direction.


import cv2
import time

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('w'):
        key = '\\frame-cradle2' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
        cv2.imwrite(filename="D:\main\learnyolov3\yolov3-master\images"+ key, img = frame)

cap.release()
cv2.destroyAllWindows()