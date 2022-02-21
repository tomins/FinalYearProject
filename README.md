# FinalYearProject
current tasks:
  - DONE Get crime data into DB
  - Create filter place
  - Get all parking by default distance(to link to filter)
  - Display crime data with parking locations - display all parking by num of crimes per year on street
  - Add price to the front of the parking location (to be added as something to filter by)
  - Add button to filter
  - Add a way to filter the parking locations by location(miles or meters from given location), price(per 1 hour maybe), crime(importance scale 1-10) 
 
 **step 1: Get Crime data into DB**
  - DONE isolate the lat,lng of a user location
  - DONE Create crime in django
  - DONE Check if this street is in the crime Db already:
  -   -DONE if yes:
  -       - DONE return this result(console log)
  -   -else:
  -       - DONE search the api for this location
  -       - DONE calculate distance from the 2 points
  -       - DONE add 1 if the points within .2 miles
  -       - DONE once the entire result is sorted through then save the street name and num of crimes committed on it(could be more complicated to add in other crimes then just                   vehicular)
  -       - DONEReturn the result of the database entry(console log)
  -       

**Step 2: Create Filter**
  - DONE Create a dropdown list with the following (All sliders)
  -   - DONE Distance slider between .2 -> 2 miles
  -   - DONE Price (minimum charge) between free -> £10
  -   - DONE Crimes between 1-10 scale
  - DONE KINDA Create method to check each of these
**Step 2.5: Gets the geolocation of each of the parkingZones**
  - DONE Add a latlng area to ParkingZone (migrate)
  - DONE When each one is found use the geocoder from google
  - DONE Will then allow step 3 to go easier
**Step 3: Get all parking within a distance**
  -Send request from vue rathe rathen by postcodre(currently in location)
  - Create a searchByDistance in views.py in parkingZone
  -   - Takes in a latLong of the users location and distance wanted
  -   - Compare distance and if less then the distance wanted then add it to the list of ParkingZones to return
  
