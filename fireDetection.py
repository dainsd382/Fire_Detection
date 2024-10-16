import cv2          # Library for openCV
import threading    # Library for threading -- which allows code to run in backend
import playsound    # Library for alarm sound
import smtplib      # Library for email sending

# To access xml file which includes positive and negative images of fire. (Trained images)
# File is also provided with the code.
fire_cascade = cv2.CascadeClassifier("fire_detection_cascade_model.xml")

# To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
vid = cv2.VideoCapture(0)
# created booleanq
runOnce = False


# defined function to play alarm post fire detection using threading
def play_alarm_sound_function():
    # to play alarm # wav audio file is also provided with the code.
    playsound.playsound("fire_alarm.wav", True)
    # to print in console
    print("Fire alarm end")

# defined function to send mail post fire detection using threading
def send_mail_function():
    # recipients mail
    recipientmail = "nguyenducdai382@gmail.com"
    # To lower case mail
    recipientmail = recipientmail.lower()

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        # Senders mail ID and password
        server.login("nguyenducdai382@gmail.com", "djzj bamt vjvh kjqw")
        # recipients mail with mail message
        server.sendmail(
            "nguyenducdai382@gmail.com",
            recipientmail,
            "Warning fire accident has been reported",
        )
        # to print in console to whom mail is sent
        print("Alert mail sent successfully to {}".format(recipientmail))
        # To close server
        server.close()

    except Exception as e:
        # To print error if any
        print(e)


while True:
    Alarm_Status = False
    # Value in ret is True # To read video frame
    ret, frame = vid.read()
    # To convert frame into gray color
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # to provide frame resolution
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    # to highlight fire with square
    for x, y, w, h in fire:
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]

        print("Fire alarm initiated")
        # To call alarm thread
        threading.Thread(target=play_alarm_sound_function).start()

        if runOnce == False:
            print("Mail send initiated")
            # To call alarm thread
            threading.Thread(target=send_mail_function).start()
            runOnce = True
        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
