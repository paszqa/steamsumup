import mysql.connector
import os
import subprocess
import time
import requests
import cloudscraper

mydb = mysql.connector.connect(
          host="localhost",
            user="loser",
              password="dupa",
                database="trackedtimes"
                )

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM `totalTimes` ORDER BY `totalTime` DESC LIMIT 25")
#print("Final total time")
f = open
print("No ; Game ; Hours ; Slavs ")
no=1
for finalRow in mycursor.fetchall():
    #print("Working on: "+str(finalRow[1]))
    gameName=subprocess.check_output('python3 /home/pi/steamsumup/getName.py '+str(finalRow[1]), shell=True)
    #print(gameName)
    gameName = str(gameName).replace("\\n\'","")
    gameName = gameName[2:].replace("\"","")
    gameName = gameName.replace("\\'","'") #fix apostrophe
    gameName = gameName.replace("\\xe2\\x84\\xa2","®")
    gameName = gameName.replace("\\xe2\\x80\\x99","'")
    gameName = gameName.replace("\\xc2","").replace("\\xae","").replace("\\xe2","")
    gameName = gameName.replace("\\n\'","")
    gameName = gameName.replace("\\n","")
    appId=str(finalRow[1])
    hours=str(round(finalRow[3]/60,2))
    players=str(finalRow[4])
    print(str(no)+";"+str(gameName)+";"+hours+";"+players)
    no+=1
