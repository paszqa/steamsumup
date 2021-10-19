import mysql.connector
import subprocess
import sys

mydb = mysql.connector.connect(
          host="localhost",
            user="loser",
              password="dupa",
                database="trackedtimes"
                )

mycursor = mydb.cursor()
#mycursor.execute("SELECT * FROM `totalTimes` ORDER BY `totalTime` DESC LIMIT 25")

#print(sys.argv[0]);
#print(sys.argv[1])
idToCheck = sys.argv[1]

#####################################
# Check if appID exists in DB
#####################################
numberOfResults = 0
mycursor.execute("SELECT `name` FROM `steamgames` WHERE `appId` = "+idToCheck)
for row in mycursor.fetchall():
    #print("A"+str(row))  
    numberOfResults += 1

#print("Results: "+str(numberOfResults))
####################################
# Get name and add if doesnt exist
####################################
if numberOfResults == 0:
    for x in range(1,10):
        #Try Steam Store
        #print("X1")
        gameName=subprocess.check_output('curl -s https://store.steampowered.com/api/appdetails/?appids='+str(idToCheck)+' | jq \'.[] | .data | .name\'', shell=True)
        #print("X2")
        #print(str(gameName))
        if str(gameName) != "b'null\\n'":
            break; #Leave if name is not empty
        #Try Steam Charts
        #print("X3")
        url = "'https://steamcharts.com/app/"+str(idToCheck)+"'"
        #print("X4")
        gameName=subprocess.check_output('curl -s '+url+' | grep -i "<title>"', shell=True)
        #Clean up the name
        gameName=str(gameName).replace(" - Steam Charts","")
        gameName=gameName.replace("Steam Charts - ","")
        gameName=gameName.replace("\\n","")
        gameName=gameName.replace("<title>","")
        gameName=gameName.replace("</title>","")
        gameName=gameName.replace("\t","")
        gameName = str(gameName[2:]).replace("\"","")
        gameName = gameName.replace("\\'","'") #fix apostrophe
        gameName = gameName.replace("\\xe2\\x84\\xa2","®")
        gameName = gameName.replace("\\xe2\\x80\\x99","'")
        gameName = gameName.replace("\\xc2","").replace("\\xae","").replace("\\xe2","")
        gameName = gameName.replace("\\n\'","")
        if(gameName != "null"):
            break;#Break if found game name
        r = requests.get(url, allow_redirects=True)
        time.sleep(4 * x)
    #Clean up the name
    gameName = str(gameName)
    gameName = str(gameName[2:]).replace("\"","")
    gameName = gameName.replace("\\'","'") #fix apostrophe
    gameName = gameName.replace("\\xe2\\x84\\xa2","®")
    gameName = gameName.replace("\\xe2\\x80\\x99","'")
    gameName = gameName.replace("\\xc2","").replace("\\xae","").replace("\\xe2","")
    gameName = gameName.replace("\\n\'","")
    #Show output
    print(gameName)
    #Add to database for future and commit if not null
    if gameName != "null":
        mycursor.execute("INSERT INTO `steamgames` VALUES (NULL, "+idToCheck+", \""+gameName+"\")")
        mycursor.execute("COMMIT;")
####################################
# Get name if it exists
####################################
else:
    mycursor.execute("SELECT name FROM `steamgames` WHERE `appId` = "+idToCheck)
    gameName = mycursor.fetchone()
    #Show output
    print(str(gameName[0]))

####################################
# Finito
####################################
mydb.close();

