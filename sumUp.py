import mysql.connector
import os

#Check if script isn't running already
def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      #print "Error: File does not appear to exist."
      return 0
fileresult = FileCheck("/tmp/sumUp.tmp")
#f = open("/tmp/sumUp.tmp", "rw+")
if fileresult == 1:
    print("Script already running")
    quit()
else:
    print("No script running")
    g = open("/tmp/sumUp.tmp", "w+")
    g.write("busy")
    g.close()


mydb = mysql.connector.connect(
          host="localhost",
            user="loser",
              password="dupa",
                database="trackedtimes"
                )

mycursor = mydb.cursor()
#Clear DB
mycursor.execute("DELETE FROM `totalTimes`")
#Add SteamIDs from ProfileList to array
steamaccounts = []
with open('/home/pi/steamsumup/profileList') as my_file:
        for line in my_file:
                    steamaccounts.append(line)
#steamaccounts = [ "76561197994977404", "76561198000030995", "76561198004729616", "76561198009810227" ] 
for steamid in steamaccounts:
    steamid = steamid.replace("\n","")
    if steamid != "":
        print("Current Steam ID: "+str(steamid))
        mycursor.execute("SELECT * FROM (SELECT  * FROM (SELECT `appId`, `playedTotal`,`date` FROM `"+steamid+"` ORDER BY `date` DESC LIMIT 1000) AS t GROUP BY `appId`) AS t2 ORDER BY `playedTotal` DESC")
        currentResult = mycursor.fetchall()
        print(".....Fetched results with current hours")
        for row in currentResult:
            print(".....Current row - appId:"+str(row[0])+" - currentTime:"+str(row[1]))
            mycursor.execute("SELECT * FROM `totalTimes` WHERE `appId` = "+str(row[0])+"")
            results = mycursor.fetchall()
            numberOfResults = len(results)
            print("......Found "+str(numberOfResults)+" existing results for appId "+str(row[0]))
            if numberOfResults == 0:
#                gameName=os.system("curl -s https://store.steampowered.com/api/appdetails/?appids="+str(row[0])+" | jq '.[] | .data | .name'");
#                print(".........Game Name: "+str(gameName))
#                gameName = str(gameName).replace("\"","")
                mycursor.execute("INSERT INTO `totalTimes` VALUES (NULL, "+str(row[0])+", NULL, "+str(row[1])+", 1)")
                print("..........Added new entry")
            else:
                print("Results")
                print(results)
                print("Row")
                print(row)
                print("New Total Time = "+str(row[1]))
                print("... + "+str(results[0][3]))
                newTotalTime = row[1] + results[0][3]
                newPlayerCount = results[0][4] + 1
#                print(str(results[0][0])+" "+str(results[0][1])+" time: "+str(row[1])+" + "+str(results[0][2])+" = "+ str(newTotalTime))
                mycursor.execute("UPDATE `totalTimes` SET `totalTime` = "+str(newTotalTime) +", `players` = "+str(newPlayerCount)+" WHERE `appId` = "+str(row[0]))
                print("..........Updated entry for appId "+str(row[0])+": "+str(row[1])+" + "+str(results[0][3])+" = "+str(newTotalTime))

mycursor.execute("COMMIT;")
mycursor.execute("SELECT * FROM `totalTimes`")
print("Final total time")
print("ID\tappId\ttotalTime\tplayers")
for finalRow in mycursor.fetchall():
    print(str(finalRow[0])+"\t"+str(finalRow[1])+"\t"+str(finalRow[2])+"\t"+str(finalRow[3]))

os.remove("/tmp/sumUp.tmp")
#g = open("/tmp/sumUp.tmp", "w")
#g.write("")
#g.close()
