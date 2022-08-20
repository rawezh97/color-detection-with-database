import numpy as np
import cvui
import cv2


#create the trackbar to make change in hsv
def trackbar(para):
	global hue_low , hue_high , satur_low , satur_high , value_low , value_high
	hue_low = cv2.getTrackbarPos('hue_low' , 'controls')
	hue_high = cv2.getTrackbarPos('hue_high' , 'controls')
	satur_low = cv2.getTrackbarPos('satur_low' , 'controls')
	satur_high = cv2.getTrackbarPos('satur_high' , 'controls')
	value_low = cv2.getTrackbarPos('value_low' , 'controls')
	value_high = cv2.getTrackbarPos('value_high' , 'controls')


hue_low = 0
hue_high = 180
satur_low = 0
satur_high = 255
value_low = 0
value_high = 255


controls = cv2.namedWindow('controls' ,  cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('hue_low' , 'controls' , 95,180 , trackbar)
cv2.createTrackbar('hue_high' , 'controls' , 135,180 , trackbar)
cv2.createTrackbar('satur_low' , 'controls' , 200,255 , trackbar)
cv2.createTrackbar('satur_high' , 'controls' , 255,255 , trackbar)
cv2.createTrackbar('value_low' , 'controls' , 55,255 , trackbar)
cv2.createTrackbar('value_high' , 'controls' , 255,255 , trackbar)



width = 800
height = 480
cam_no = 1

def create_camera (channel):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # ID number for width is 3
    cap.set(4, 480)  # ID number for height is 480
    cap.set(10, 100)  # ID number for brightness is 10qq
    return cap
cam = create_camera(str(cam_no))
cvui.init('screen')
while True:
    success, current_cam = cam.read()
    dim = (width, height)
    frame = cv2.resize(current_cam, dim, interpolation=cv2.INTER_AREA)
    cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    if (cvui.button(frame, width - 200, height - 40, "Blue") and cvui.mouse(cvui.CLICK)):
        cvui.init('screen')
        hue_low = 95
        hue_high = 135
        satur_low = 200
        satur_high = 255
        value_low = 55
        value_high = 255
	
    min_HSV = np.array([hue_low , satur_low , value_low])
    max_HSV = np.array([hue_high , satur_high , value_high])

    # if in boleean we got a false that is meant we don't have a frame
    # we don't want this program is be stoped we want continue for this moment
    if not success:
	        continue

    # we change the BGR type of color to HSV type on every single frame
    image = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

    #this founction make a object be white and background of it be black
    mask = cv2.inRange(image , min_HSV , max_HSV)
    res = cv2.bitwise_and(frame, frame, mask=mask)


        # Note : this to variable over uesing to show and pop up to the screen
        # we use { imshow } founction to pop up the new wendow of our vraiable
        # if you don't got it check line (144)

        # this founction rghit here make two list or return a two list into this two variable
        # contours have list of object ( one frame can have many object ) this founction create a list of object
        #
    contours , hier = cv2.findContours(mask , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

        # we need this empty list just for got it how this detection work
    detect = []

        # wen can have many object on one frame that is why we need to create a ( for loop )
        # we want to detect evry object on the frame
    for i in contours :

    			#this founction contour area to the object
            area = cv2.contourArea(i)

    			# we don't want detect evry single object in this case we work on (rubick's cube)
    			# that is why we use 800 if you work with a bigger thing you can rise the number 800 to the waht you want
            if area > 800 :

                    # we get the x , y , wiedth , high with this founction
                x,y,w,h = cv2.boundingRect(i)
                detect.append([x,y,w,h])

                    # this to variable is the most important thing on this project
                    # that alow the red point to be always be in the center of object
                f = int(( x + x + w ) / 2)
                g = int(( y + y + h ) / 2)

                    # if you want see the evry single change of x,y,w,h of object do this > print(detect)

                    # this founction make a red point on the object
                    # (f,g) our to variable and condition and the 5 (0,0,255) is a Blue,Green,Reed
                    # and you can change the 5 and -1 and see what is it do
                cv2.circle(frame ,(f , g), 5 ,(0,0,255),-1 )

                    # this make a grren rectangle around the object
                    # (x,y) is a x , y of object on the frame (top of left)
                    # (x+w , y+h) is that point rectangle is done (bottom of right)
                cv2.rectangle(frame , (x,y) , (x +w , y+h) ,(0 , 200 , 0) , 5)
                    #cv2.putText(frame ,str(count_frame) ,(3 , 80 ), cv2.FONT_HERSHEY_DUPLEX, 1.0 , (0,0,0) , 1)

    cv2.imshow('screen', frame)
    cv2.imshow('image' , mask)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
