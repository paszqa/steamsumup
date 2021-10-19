#Imports
import os
from PIL import Image, ImageDraw, ImageFont

#Choose size and color
#img = Image.new('RGB', (550, 400), color = (73, 109, 137))
img = Image.open('background.png')
img = img.convert("RGB")
#Choose fonts
fnt = ImageFont.truetype('/home/pi/steamsumup/ShareTechMono-Regular.ttf', 15)
#Settings
rowHeight=15


#Draw background
d = ImageDraw.Draw(img,'RGBA')

#Get text from file
f = open('latest-slav-top.csv','r')

#Analyze each line from the file
rowNumber = 0
for row in f:
    rowSplit = row.split(";")
    if rowNumber == 0:
        currentColor = (122,122,122) #grey
    elif rowNumber == 1:
        currentColor = (49, 199, 38) #green
    elif rowNumber == 2:
        currentColor = (169, 199, 38) #light green
    elif rowNumber == 3:
        currentColor = (199, 194, 38) # yellowish
    else:
        currentColor = (199, 140, 38) #orange
    d.text((10,rowHeight*rowNumber), rowSplit[0], font=fnt, fill=currentColor)
    if rowNumber % 2:
        d.rectangle([(10,rowHeight*rowNumber),(500,rowHeight*(rowNumber+1))], fill=(0,0,0,57))
    d.text((50,rowHeight*rowNumber), rowSplit[1][0:45], font=fnt, fill=currentColor)
    d.text((430,rowHeight*rowNumber), rowSplit[2], font=fnt, fill=currentColor)
    d.text((480+min(1,rowNumber)*15,rowHeight*rowNumber), rowSplit[3], font=fnt, fill=currentColor)
    rowNumber += 1
#Save for the glory of Slav Squat Squad
img.save('latest-slav-top.png')
