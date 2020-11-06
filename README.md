# sw-csv
 play with the star wars api and manipulate csv data 
 
 
 ### Features

*Note: developed using Python 3.6.6*

Fetch people from https://swapi.dev

Apply some transformations on data using the Petl library and save it as CSV.
*date is added and transform to a correct format, homeworld names are resoleved and unused fields are removed*

the maine url path is at http://127.0.0.1:8000/ and usable with the django runserver.
first click on Fetch and wait until a csv is generate.
After that you will be able to click on date to explore a collection of SW people. 
The collection table load people 10 by 10 using the load more button.
You can download the full collection csv by clicking the uuid csv name on top. 
