import cv2
import smtplib
import imghdr
from email.message import EmailMessage
from playsound import playsound

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')  #importing the xml files
mail_content = '''Fire Alert!!! Call the Fire department'''
message = EmailMessage()

sender = '###@gmail.com'
receiver = '###@gmail.com'
message['From'] = sender
message['To'] = receiver
message['Subject'] = 'ALERT! FIRE AT HOME!'

img_counter = 0
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) #multiscale is used to detect objects of different sizes and draw a rectangle around it. First argument is input. second is the scalefactor (how much the image size will be reduced at each image scale). third is the width of the rectangle

    for (x, y, w, h) in fire:   # loops through each frame detected
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2) #drawing a rectangle 
        roi_gray = gray[y:y + h, x:x + w] # graphically selects the region of interest
        roi_color = frame[y:y + h, x:x + w]
        print("fire is detected")
       # playsound.playsound('Alarm Sound1.mp3',True)
        img_name = "Capture_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{}".format(img_name))
        img_counter += 1

        with open(img_name, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
            message.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
        mail_server.login("##@gmail.com", '###')
        mail_server.send_message(message)
        mail_server.quit()
        print('Mail Sent')

    cv2.imshow('Camera', frame)
    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cam.release()    
