#Camera video capture, while running this code, it show the Camera video, at the same time it will also capturing the video, if you press q button it will stop capturing and save the file call handsomeboy.avi in your direction.


import cv2
import time

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    laplacian_var = cv2.Laplacian(frame, cv2.CV_64F).var()
    cv2.imshow('frame', frame)


    if laplacian_var <470 :
        print ("photo is blurry")
    else:
        print("photo is good" + str(laplacian_var))


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif (cv2.waitKey(1) & 0xFF == ord('w')) and (laplacian_var >= 470) :
        key = '\\frame-cradle2' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
        cv2.imwrite(filename="D:\main\learnyolov3\yolov3-master\images"+ key, img = frame)





cap.release()
cv2.destroyAllWindows()