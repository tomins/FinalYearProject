# FinalYearProject
current tasks:
  - DONE Get crime data into DB
  - Create filter place
  - Display crime data with parking locations - display all parking by num of crimes per year on street
  - Add price to the front of the parking location (to be added as something to filter by)
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
  - Create a dropdown list with the following (All sliders)
  -   - Distance slider between .2 -> 2 miles
  -   - Price (minimum charge) between free -> £10
  -   - Crimes between 1-10 scale
  - Create method to check each of these
  
