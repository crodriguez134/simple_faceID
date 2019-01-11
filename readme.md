# simple_faceID
Messing around with facial recognition in Python.


                                                      Installation

This code was written and tested in a linux environment, so some functions may not translate well to other operating systems. It
hasn't been run outside of an IDE so far, so I highly recommend using one if you're interested in this project. My preferred IDE 
is Pycharm, it was confusing at first but I've grown to like it. You can find the download link here:

https://www.jetbrains.com/pycharm/download/#section=linux


Make sure you have python3 installed on your system before you begin. You should be able to run 

> $ python3

in the terminal. You'll get a message with the version number, some pointers as to what you can type, and the $ sign becomes >>>.
Type in

">>>" quit()

to exit that screen and go back to a normal terminal. If the command python3 doesn't work, install python3 using:

> $ sudo add-apt-repository ppa:jonathonf/python-3.6

> $ sudo apt-get update

> $ sudo apt-get install python3.6

Now, create a directory for the project, and in that directory, create a virtual environment (venv). You can use the command:

> $ python3 -m venv /path/to/new/virtual/environment

to create the directory and virtual environment at the same time. Note: you may need to run the command with "sudo", so that it 
reads "sudo python3 -m....."

Place the python files that you're interested in from this repository into that directory. Make sure to include the requirements.txt
file in the directory. Now run the following commands:

> $ cd /path/to/virtual/environment

> $ sudo pip install -r requirements.txt

The terminal should begin to install the required packages, and will likely prompt you to agree to installs. When all of that 
finishes, hopefully everything works. Unfortunately, I know that opencv3 has problems when you try to install it via pip. 

If you're facing problems, look up the errors online and follow whatever you find. If opencv isn't playing nice, try this method
for installing it:

> https://gist.github.com/Mahedi-61/804a663b449e4cdb31b5fea96bb9d561


                                                Description of Each Project

          active_faceID_retry.py

Takes in a known image from memory, compares a face capture taken from the webcam, and determines if they're the same face or not. It writes the name of the person it detects above the face detection rectangle.

          faceID_simple.py

Removed the GUI, used espeak to have it talk to the user. This project recognizes a face, identifies it, then, if it's a known
face, it greets the user. Otherwise, it tells the user it does not recognize them.

          multi_faceID.py
      
Same thing as faceID_simple.py except with the added option to add your face via the program instead of in the backend code/files.
Uses memory and an os.walk() to organize images and labels. This code is too slow for use on a Raspberry Pi though.

          multi_faceID_lightweight.py
     
Performance optimizations on multi_faceID.py. For example, each known person's image is only encoded once. The encoded image
data is stored into memory using pickle, then retrieved and put into a dictionary upon startup. I found that encoding images 
using the face_recognition library took up a lot of time, so it helps to only have to encode twice (once for a known image and
once for an unknown image). 



