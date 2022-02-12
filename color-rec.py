from datetime import datetime
import numpy as np #pip install numpy
import pyodbc #pip install pyodbc
import cv2 #pip install opencv-python
import os

#This Program must be using with python3.9.7 or earlier
#                           in here you must change (Server=your Server name; Database=your database name)
connection = pyodbc.connect('Driver={SQL server};Server=DESKTOP-34E9PTT;Database=rawezh;Trusted_Connection=yes;')
dbfunction = connection.cursor()

# 95 in min_HSV and 135 in max_HSV is a Hue (color it self) you can change for anithing you want
# 200 and 255 of both is a Saturation
# last 55 and 255 is a value
# for understand this search it for { hsv color }
min_HSV = np.array([95 , 200 , 55])
max_HSV = np.array([135 , 255 , 255])

# in here we capture the video
#if you don't want use your webcam and you want use your own video you can do like This
#change the 0 to "path your video"
#for example  video_capture = cv2.VideoCapture("my_video.mp4")
video_capture = cv2.VideoCapture("Rubik.mp4")

#we need thi tow variables to go with the flow(-_-)
count_frame = 0
rise = 34

# video work with a frame, one video have a lot of frame which make a video show
# that is why we need a ( while loop ) because we work with every single frame one by one
# if you want to be better on it check this out https://www.youtube.com/watch?v=dEtiNxlTJ8I
while True:

	# this founction return to value one of them is a ( true and false ) and we put this value to boleean variable
	# and frame variable have a realy frame
	boleean , frame = video_capture.read()

	# if in boleean we got a false that is meant we don't have a frame
	# we don't want this program is be stoped we want continue for this moment
	if not boleean:
		continue

	# we change the BGR type of color to HSV type on every single frame
	image = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

	#this founction make a object be white and background of it be black
	mask = cv2.inRange(image , min_HSV , max_HSV)

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
				count_frame +=1

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

				# if we dont put on the condition on this capture image then the program send a lot of unless data to Database
				# we want take a picture evry 25 frame taht is nearle about 1 secound  that is meant evry secound we take a pictre of our target we pass through around
				# you can change this condition
				if count_frame == rise :
					print ("Sucsess")

					# capture image
					capture = frame[y:y + h, x:x + w]
					# we try to make a uniqe name for ech object by this function
					name=str(w+h+x) + '_oject.jpg'
					# this function save image on that folder your python file is
					saving= cv2.imwrite(name, capture)


					# to get local time
					local_time = datetime.now()
					date = local_time.strftime("%d/%m/%Y")
					time = local_time.strftime("%H:%M:%S")

					# we have this table on sql server and our database
					'''
					create table capture_img (
					id int identity ,
					obj_name varchar(25),
					date2 varcahr(25),
					time2 varcahr (25),
					img varbinary(max)
					)
					'''
					# in here you must be change the path that your file have it in my computer it is on the desktop that is why we enter this path 	C:\\Users\\dbms3\\Desktop\\colo-rec\\     Note :we must split by [\\] not a single one [\]
					# Note: don't change {name} in the end of the path just change path befor {name}
					# this founction used for send our image we captured and name and date to the sql server
					# for better got it looking for (varbinary data type) and (bulk column in sql server)
					dbfunction.execute(f'''INSERT INTO capture_img (obj_name,date2,time2,img) SELECT '{name}' as filename ,'{date}' as date,'{time}' as time, BulkColumn FROM Openrowset(Bulk 'C:\\Users\\dbms3\\Desktop\\colo-rec\\{name}', Single_Blob) as image''')

					# this is a another important function that remove the image we captured beffor after send a picture we don't need it any more we must delete it by this founction
					os.remove(name)
					# *Note that commit/rollback is always performed at the connection level. pyodbc provides a commit/rollback method in the cursor objects, but they will act on the associated connection.
					connection.commit()

					# if frame == 34 ; want to add 34 to the rise because we want after 34 frame later just capture one image about 1 secound
					rise += 34

				# we want continue with other frame without capture anything
				else :
					continue


	# we need this founction to pop up the wendow on the screen
	# ("mask") it is just a name of wendow you can change to anything you want
	#( "video" , frame ) "video" is also a name but frame and mask in here that variable we decleared in line (36,47)
	cv2.imshow("mask" , mask)
	cv2.imshow("video" , frame)


	# in here we want by defult program work if we press the up navebar the programm will be end
	# you can change cv2.waitKey(0) in this case program will work when you press a key on your keyboard
	key = cv2.waitKey(1)
	if key == 0 :
		dbfunction.close()
