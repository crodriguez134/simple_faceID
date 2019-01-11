# Simple face identification, only compares against one image. Finishes running in less than 1.1 seconds.

import cv2
import face_recognition as fr
import os

frontal_face_cascade = cv2.CascadeClassifier("/home/usr/opencv/Opencv_Cascades/haarcascade_frontalface_alt2.xml")

known = fr.load_image_file("/home/usr/PycharmProjects/Project_Name/venv/img_train/img_name/img8.JPG")

known_encoding = fr.face_encodings(known)[0]

green = (0, 255, 0)
white = (255, 255, 255)
stroke = 2
name = "User"
font = cv2.FONT_HERSHEY_SIMPLEX

detected = False


def check_for_face():
    video = cv2.VideoCapture(0)

    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("pic.jpg", gray)
    im = cv2.imread("pic.jpg")
    face_locations = fr.face_locations(im)

    if len(face_locations) == 0:
        os.remove("pic.jpg")
        video.release()
        return None
    else:
        face = fr.load_image_file("pic.jpg")
        os.remove("pic.jpg")
        video.release()
        return face


def id_face(unknown_face):
    # Prepare the image of the face to be encoded
    cv2.imwrite("unknown.jpg", unknown_face)
    unknown = fr.load_image_file("unknown.jpg")
    os.remove("unknown.jpg")

    # Encode the image of the face
    unknown_encodings = fr.face_encodings(unknown)

    if len(unknown_encodings) > 0:
        unknown_encoding = unknown_encodings[0]
    else:
        print("no face detected")

    results = fr.compare_faces([known_encoding], unknown_encoding)

    if results[0]:
        return "User"
    else:
        return "unknown"


def program_run():
    run = input("Run the program? (y/n)")

    if run == "y":
        print("Checking for a face...")

        id = check_for_face()
        timeout = 0

        # Set a loop to run the check_for_face() function until it finds a face. If it can't find a face, timeout and
        # prompt the user to ask if they want to run the program again or not.
        while id is None:
            id = check_for_face()
            if timeout == 10:
                response = input("Could not find face. Try again? (y/n)")
                if response == "y":
                    print("Checking for a face...")
                    timeout = 0
                else:
                    quit()
            timeout += 1

        name = id_face(id)

        if name == "User":
            greeting = "Hello " + name + ", nice to see you."
            os.system("espeak '{}'".format(greeting))

        else:
            greeting = "Hello there, I dont think we have met before."
            os.system("espeak '{}'".format(greeting))
    else:
        print("okay")
        quit()


program_run()
