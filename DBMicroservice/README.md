# Data Base Microservice using Python Flask and SQL Alchemy
1. Set up the database. One you have loaded the script in, open up a command prompt and navigate to the app.py directory. Run the following set of commands to initilize and create a local instance of the database called budget.db.
```
cd DBMicroservice
python # open python terminal
from app import db # this will import the sqlite database from SQLAlchemy
db.create_all()
exit()
```
2. Initlize the service by running the following command within the directory.
```
python app.py
````
This will create a path for your browser at http://localhost:5000/. Since there is no home page, navigate to http://localhost:5000/budget.