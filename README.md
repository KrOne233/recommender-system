# recommender-system
A restaurant recommender system based on the CO2 emission of the food in the menu, as well as the customer ratings.

The system is built under the framework of Django. 

Notice that the system need MySQL support, please install the database and change the database settings in the file 
```bash
recommendersystem/settings.py
```
and delete the files with number in front under directory
```bash
restaurant_system/migrations
```
and run
```bash
python manage.py makemigrations
python manage.py migrate
```

The data is scraped from the websites including the user information, and therfore can not be published.

The recommender is achieved based on colleberative filtering, using matrix-factoriztion SVD. The training process is in the file:
```bash
restaurant_system/CF.py
```

## run the system
```bash
python manage.py runserver
```

You can login as the administrator in following link:
```bash
http://127.0.0.1:8000/admin/
username = admin
password = admin
```

The link for user login and Sign Up
```bash
http://127.0.0.1:8000/restaurant_system/login/
```
