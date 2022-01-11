#Katherine Zhang    UCID:
#This program tracks the path of a hurricane/storm and displaus the category and maximum wind speed.
from SimpleGraphics import *

#Resizing graphics window to 1022 x 620
resize(1022, 620)

#Display map
img = loadImage("map.gif")
drawImage(img, 0, 0)

#Fixing Majic Numbers
latvalue = 95
xspacing = getWidth()/9
x = xspacing
yspacing = getHeight()/5
y = yspacing
longvalue = 35

#Assigning variables to compare to max category and max wind speed.
maxwindSpeed = 0
printcategory = 0

#Draw lines for latitude and longitude using while loop
setColor("gray")
#Latitude lines
lineNum = 8
while lineNum > 0:
    line(xspacing, 0, xspacing, getHeight())
    latvalue = latvalue - 5
    text(xspacing - 15, 10, str(latvalue) + "W")
    xspacing = x + xspacing
    lineNum = lineNum - 1

#Longitude lines
lineNum = 4
while lineNum > 0:
    line(0, yspacing, getWidth(), yspacing)
    longvalue = longvalue - 5
    text(15, yspacing - 8, str(longvalue) + "N")
    yspacing = y + yspacing
    lineNum = lineNum - 1

#Read longitude and latitude from user
latitude = float(input("Enter the latitude in degrees North of the equator: "))

#Plot path of storm on graph
numPoint = 0
while latitude != 0:
    longitude = float(input("Enter the longitude in degrees West of the prime meridian: "))
    newWindSpeed = float(input("Enter the wind speed in mph: "))

    #Convert latitude and longtitude to position on graph
    y = getHeight() - (latitude - 10) * (getHeight()/25)
    x = (longitude + 95) * (getWidth()/45)
    #Adding color and size
    #Category 5
    if newWindSpeed >= 157:
        category = 5
        color = setColor("purple")
        diameter = 15
        plotpoint = ellipse(x, y, diameter, diameter)
    #Category 4
    elif 130 <= newWindSpeed < 157:
        category = 4
        color = setColor("red")
        diameter = 13
        plotpoint = ellipse(x, y, diameter, diameter)
    #Category 3
    elif 111 <= newWindSpeed < 130:
        category = 3
        color = setColor("orange")
        diameter = 11
        plotpoint = ellipse(x, y, diameter, diameter)
    #Category 2
    elif 96 <= newWindSpeed < 111:
        category = 2
        color = setColor("yellow")
        diameter = 9
        plotpoint = ellipse(x, y, diameter, diameter)
    #Category 1
    elif 74 <= newWindSpeed < 96:
        category = 1
        color = setColor("green")
        diameter = 7
        plotpoint = ellipse(x, y, diameter, diameter)
    #Category 0
    else:
        category = 0
        color = setColor("gray")
        diameter = 5
        plotpoint = ellipse(x, y, diameter, diameter)

    #Connecting the points on the map
    if numPoint != 0:
        line(previousx + diameter / 2, previousy + diameter / 2, x + diameter / 2, y + diameter / 2)

    #Counting number of points drawn on map.
    numPoint = numPoint + 1

    #Categorizing the storm and max. wind speed.
    if newWindSpeed > maxwindSpeed:
        maxwindSpeed = newWindSpeed
    if category > printcategory:
        printcategory = category

    #Store previous x and y values to connect the points on the map
    previousx = x
    previousy = y

    #Read another input from user:
    latitude = float(input("Enter the latitude in degrees North of the equator (0 to quit): "))

#Displaying category of the storm
setColor("white")
text(940, 25, "Max. Category: %.0f"  % printcategory)
#Display max. wind speed
text(910, 45, "Max. Wind Spped (mph): %0.1f" % maxwindSpeed)
