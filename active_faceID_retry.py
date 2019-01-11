import cv2
import face_recognition as fr
import os

video = cv2.VideoCapture(0)

frontal_face_cascade = cv2.CascadeClassifier("/home/usr/opencv/Opencv_Cascades/haarcascade_frontalface_alt2.xml")

known = fr.load_image_file("/home/usr/PycharmProjects/Project_Name/venv/img_train/img_name/img8.JPG")

known_encoding = fr.face_encodings(known)[0]

green = (0, 255, 0)
white = (255, 255, 255)
stroke = 2
name = "User"
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = frontal_face_cascade.detectMultiScale(gray, 1.05, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        cv2.imwrite("unknown.jpg", roi_gray)
        unknown = fr.load_image_file("unknown.jpg")
        os.remove("unknown.jpg")

        unknown_encodings = fr.face_encodings(unknown)

        if len(unknown_encodings) > 0:
            unknown_encoding = unknown_encodings[0]
        else:
            print("no face detected")
            continue

        results = fr.compare_faces([known_encoding], unknown_encoding)

        if results[0]:
            cv2.putText(frame, name, (x, y), font, 1, white, stroke, cv2.LINE_AA)
        else:
            cv2.putText(frame, "unknown", (x, y), font, 1, white, stroke, cv2.LINE_AA)

        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), green, stroke)

    cv2.imshow('Capturing', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

