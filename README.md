# Deep_learning_color_detection_connect_with_database
.......................................... Color-Detection ..................................................................


# Color Detection
this program can detect any color and after detect the object  
it take a picture and send to the SQLServer database stroed in there  
also can detect multiple object in the same time  


Thanks for god finaly done 

# Requerments

first if you have the SQLServer thats be good 
if not download from here [SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads). or anywhere you want 

# Usage
-this Program must be useing with python 3.9 or erliaer
- first you must install library 
```
 pip install pyodbc
 pip install opencv-python
 pip install numpy
 ```
 # Connect to SQLServer database
 
 change this part to your own [server-name] and [dataase-name]
 ```
 connection = pyodbc.connect('''
				Driver={SQL server};
				Server=Server_name;
				Database=Database_name;
				Trusted_Connection=yes;
				''')
```
**Example how it be like** 

**Note** : if you use username and password to your SQLServer This part must be like this  
```
connection = pyodbc.connect('''
				Driver={SQL server};
				Server=DESKTOP-25E9PTT;
				Database=colorDB;
				UID = your-username;
        PWD = your-password;
				''')
```

# Createing table
inside you SQL-Server database after using you database  
you shuld crate a table for the programm the table must be like this
```
create table capture_img ( id int identity ,
                           obj_name varchar(25),
                           date2 varcahr(25),
                           time2 varcahr (25),
                           img varbinary(max));
```
 
 
 
# changing color

***you must change this part to what color you want***
if you don't know about what shuld you do check this out [HSV](http://color.lukas-stratmann.com/color-systems/hsv.html).  
```
min_HSV = np.array([95 , 200 , 55])  
max_HSV = np.array([135 , 255 , 255])  
```

***For Example***  
if we want detect the **green** color we must do like tis  
```
min_HSV = np.array([55 , 200 , 55])  
max_HSV = np.array([65 , 255 , 255])  
```
![HSV](https://user-images.githubusercontent.com/92225352/181918103-b4f39751-f5d7-4cad-a524-8d1f1943d495.png)





# Example how it work

**just fetect a blue color in this case**
   
![Screenshot at 2022-07-30 16-22-11](https://user-images.githubusercontent.com/92225352/181914679-b2b5c609-2597-4e88-b6f7-799d5af85102.png)

***This programm can detect the multiple object in the same time***


![Screenshot at 2022-07-30 16-23-17](https://user-images.githubusercontent.com/92225352/181914722-5b26ab69-df35-4f64-8729-ca21872abb23.png)

# view image
to see that picture this pprogramm taked we need a [SQL image viewer](https://www.yohz.com/siv8_details.htm)


