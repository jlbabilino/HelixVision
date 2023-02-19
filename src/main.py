import cv2 as cv
import time

print(cv.getBuildInformation())

fps_start_time = 0

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    # Compute FPS and print to screen
    fps_end_time = time.time()
    time_diff = fps_end_time - fps_start_time
    fps = 1/(time_diff)
    fps_start_time = fps_end_time
    fps_text = "FPS: {:.2f}".format(fps)
    cv.putText(img, fps_text, (5,30), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 1)

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Detect 16h5 markers and draw bouding boxes/ids
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_APRILTAG_16h5)
    parameters =  cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)
    corners, ids, _ = detector.detectMarkers(img)
    cv.aruco.drawDetectedMarkers(img, corners, ids)

    # Display the resulting frame
    cv.imshow('frame', img)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
