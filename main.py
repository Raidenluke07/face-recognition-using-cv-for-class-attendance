import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
from pathlib import Path

path = "C:/Users/Raiden/Downloads/Face-Recognition-Attendance-Projects-main/Face-Recognition-Attendance-Projects-main/Training_images"
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    file_path = 'Attendance.csv'

    # Check if the file exists; if not, create it with the header
    file_exists = Path(file_path).is_file()
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)

        # Write header if the file is newly created
        if not file_exists:
            writer.writerow(['Name', 'Time'])

        # Write name and time to the CSV file only if the person is recognized
        if name != 'UNKNOWN':
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            writer.writerow([name, dtString])
            print(f"Attendance recorded for {name} at {dtString}")
        else:
            print("Unknown person detected. Attendance not recorded.")


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Set a threshold for face recognition
    threshold = 0.6

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=threshold)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        if True in matches:
            matchIndex = matches.index(True)
            name = classNames[matchIndex].upper()
            face_distance = faceDis[matchIndex]

            if face_distance <= threshold:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
            else:
                print("Face detected, but not recognized as a known person.")
        else:
            print("Unknown person detected.")

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)



def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    file_path = 'Attendance.csv'

    # Check if the file exists; if not, create it with the header
    file_exists = Path(file_path).is_file()
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)

        # Write header if the file is newly created
        if not file_exists:
            writer.writerow(['Name', 'Time'])

        # Write name and time to the CSV file only if the person is recognized
        if name != 'UNKNOWN':
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            writer.writerow([name, dtString])
            print(f"Attendance recorded for {name} at {dtString}")
        else:
            print("Unknown person detected. Attendance not recorded.")


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
# Set a threshold for face recognition
threshold = 0.6

for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
    matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=threshold)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

    if True in matches:
        matchIndex = matches.index(True)
        name = classNames[matchIndex].upper()
        face_distance = faceDis[matchIndex]

        if face_distance <= threshold:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
        else:
            print("Face detected, but not recognized as a known person.")
    else:
        print("Unknown person detected.")


    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
