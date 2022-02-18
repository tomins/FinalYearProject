# FinalYearProject
current tasks:
  - Get crime data into DB
  - Display crime data with parking locations - display all parking by num of crimes per year on street
  - Add price to the front of the parking location (to be added as something to filter by)
  - Add a way to filter the parking locations by location(miles or meters from given location), price(per 1 hour maybe), crime(importance scale 1-10) 
 
 **step 1: Get Crime data into DB**
  DONE isolate the lat,lng of a user location 
  - Check if this street is in the crime Db already:
  -   -if yes:
  -       - return this result(console log)
  -   -else:
  -       - search the api for this location
  -       - remove anything from the results that isn't on the right street(will require string comprehension on each street)
  -       - create a list that counts the num of occurences of crimes on tha street.
  -       - once the entire result is sorted through then save the streeet name and num of crimes committed on it(could be more complicated to add in other crimes then just                   vehicular)
  -       - Return the result of the database entry(console log)
  -       
