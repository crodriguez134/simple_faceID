import cv2
import face_recognition as fr
import os
import shutil

frontal_face_cascade = cv2.CascadeClassifier("/home/usr/opencv/Opencv_Cascades/haarcascade_frontalface_alt2.xml")

pics = {}
encoded_pics = {}
exclude = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "img_train")


# This checks the directories of images and adds images in any directory that has not yet been walked through to the
# dictionary of encoded images and names
def update_memory():
    for root, dirs, files in os.walk(image_dir, topdown=True):
        [dirs.remove(d) for d in list(dirs) if d in exclude]  # Ignore the dirs that have been added already
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG"):
                path = os.path.join(root, file)
                label = os.path.basename(root.replace(" ", "-").lower())
                exclude.append(label)
                pics[label] = fr.load_image_file(path)

    for key, value in pics.items():
        temp = fr.face_encodings(value)
        if len(temp) > 0:
            encoded_pics[key] = temp[0]
        else:
            continue


green = (0, 255, 0)
white = (255, 255, 255)
stroke = 2
name = "User"
font = cv2.FONT_HERSHEY_SIMPLEX

detected = False


# Takes a picture, creates a new directory in the proper spot and stores the image in that directory. Assigns the name
# given as the name of the new folder.
def new_face(n):
    os.system("espeak 'Please bring your face close to the camera'")

    id = check_for_face()

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

    cv2.imwrite("new_person.jpg", id)
    # newf = fr.load_image_file("new_person.jpg")
    newdir = image_dir + "/" + n
    os.mkdir(newdir)
    shutil.move("new_person.jpg", newdir)


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

    for k, v in encoded_pics.items():
        results = fr.compare_faces([v], unknown_encoding)
        if results[0]:  # If a match is found, return it
            return str(k)

    return "unknown"  # This is only reached if no match is found, so return "unknown" in that case


def program_run():
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

    if name == "unknown":
        greeting = "Hello there, I dont think we have met before."
        os.system("espeak '{}'".format(greeting))
        os.system("espeak 'Would you like me to remember your face?'")
        response = input("(y/n)")
        if response == "y":
            r = input("What is your name?")
            new_face(r)
            update_memory()
            os.system("espeak 'Your face has been saved, {}. I will remember you from now on.'".format(r))
    else:
        greeting = "Hello " + name + ", nice to see you."
        os.system("espeak '{}'".format(greeting))


run = input("Run the program? (y/n)")

if run == "y":
    print("Initializing...")
    update_memory()
    program_run()
else:
    quit()

response = input("Run again? (y/n)")

while response == "y":
    program_run()
    response = input("Run again? (y/n)")
quit()
