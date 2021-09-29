import urllib.request
import requests
f = open("key", "r")
key = f.read()
steamId = '76561198000030995'
url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+key.strip()+"&steamid="+steamId+"&format=xml&include_appinfo=1&include_played_free_games=1"
print(url)
f = open(steamId+".csv","w")
content = str(requests.get(url).content)
content = content.replace("\\n","\n").replace("\\t","\t")
f.write(content)
f.close
f = open(steamId+".csv","r")
target = open(steamId+"-2.csv","w")
content = f.readlines()
for line in content:
    if 'xml version' not in line and "game_count" not in line and "response>" not in line and "<games>" not in line and "</games>" not in line and "<message>" not in line:
        line = line.replace("\n","").replace("\t","").replace("/message>","\n").replace("&amp;","&").replace("&apos;","'")
        target.write(line)
    else:
        print("####################################HOHOHOHO"+line)
#print(content)
#f.write(str(requests.get(url).content))

#REMOVE NEWLINES AND TABS AND SHIT
#	cat $filename |grep -ivE "xml version|game_count|response>|<games>|</games>|<message>"|tr -d '\n'|tr -d '\t' > $filenameTemp
	#ADD NEWLINES TO XML AT END OF MESSAGE
#	sed -i 's#</message>#</message>\n#g' $filenameTemp
	#REMOVE AMPS
	#sed -i 's#\&amp;#\&#g' $filenameTemp
	#FIX APOSTROPHES
#	sed -i "s#\&apos;#'#g" $filenameTemp
#	echo "Done."
#print (response.status_code)
#print (response.content)
