# Resourceful Chef
The Resourceful Chef main Program and microservices were written using Flask, Python, MongoDB, HTML, and CSS.

The main program makes requests to each microservice using REST APIs. 

Each microservice either has its own MongoDB database or receives a copy of data from the main program.

Main Program - app.py located in main Resourceful Chef directory
  * includes a recipe library where the user can save their favorite recipes
  * includes a "pantry" where the user catalogues ingredients they have available in their pantry or refridgerator
  * includes a recipe journal where users can record ratings of the recipes they have made 

Request Recipe Microservice:
  * app.py located in Recipe Request Microservice directory
  * allows user to request a recipe or recipes with the greatest number of ingredients that they have available in their pantry
  * returns the name of the most resourceful recipe or recipes they have entered in their recipe library

Dates-Notes Microservice:
  * app.py located in Journal Dates-Notes Microservice directory
  * part of the Main Program's Recipe Journal
  * allows user to record dates they made a recipe and notes about a recipe they made
  * Records are displayed on pages
  * Records are saved in their own MongoDB database

Login-Logout Microservice:
  * app.py located in Login-Logout Microservice directory
  * allows user to create username and password, on successful creation logins stored in MongoDB Database
  * allows user to enter their username and password
  * when login attempt is made, username and password are confirmed with logins stored in MongoDB Database

Sort Ratings Microservice:   (written by teammate Courtney Sanders)
  * sort-microservice.py located in Rating Sort Microservice directory
  * allows the user the sort the list of recipe ratings they have previously entered so that they are displayed from highest-lowest rating, lowest to highest rating, A-Z, or Z-A

