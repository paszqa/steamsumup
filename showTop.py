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
print(" appId ; Game ; Hours ; Slavs ")
for finalRow in mycursor.fetchall():
    for x in range(1,10):
        gameName=subprocess.check_output('curl -s https://store.steampowered.com/api/appdetails/?appids='+str(finalRow[1])+' | jq \'.[] | .data | .name\'', shell=True)
#        print(str(gameName))
        if str(gameName) != "b'null\\n'":
            break; #Leave if name is not empty
#        print("Trying steamcharts");
        url = "'https://steamcharts.com/app/"+str(finalRow[1])+"'"
        gameName=subprocess.check_output('curl -s '+url+' | grep -i "<title>"', shell=True)
#        gameName=gameName.split("\n")
#        for line in gameName:
#            if "<title>" in line:
#                gameName=line
#                break;
        gameName=str(gameName).replace(" - Steam Charts","")
        gameName=gameName.replace("<title>","")
        gameName=gameName.replace("</title>","")
        gameName=gameName.replace("\t","")
#        print("!!!"+gameName)       
        if(gameName != "null"):
            break;
        r = requests.get(url, allow_redirects=True)
        time.sleep(4 * x)
        #print("Retrying ["+str(x)+"] attempt to fetch game name (appId: "+str(finalRow[1])+")")
#    gameName=str(gameName).split(";")
    gameName = str(gameName)
#    print(gameName)
    gameName = str(gameName[2:]).replace("\"","")
    gameName = gameName.replace("\\'","'") #fix apostrophe
    gameName = gameName.replace("\\xe2\\x84\\xa2","®")
    gameName = gameName.replace("\\xe2\\x80\\x99","'")
    gameName = gameName.replace("\\xc2","").replace("\\xae","").replace("\\xe2","")
    gameName = gameName.replace("\\n\'","")
    appId=str(finalRow[1])
    hours=str(round(finalRow[3]/60,2))
    players=str(finalRow[4])
    print(appId+";"+str(gameName)+";"+hours+";"+players)
