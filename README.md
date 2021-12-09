## Steps to start the app (Steps 2 and 3 is only required for the initial setup):

1) Make sure that MySQL 8.0+ is running on your system
2) If you have Anaconda, create virtual environment using ``conda env create -f environment.yml``. Or, create a Python 3.6+ environment with Django 3.2.8. Then, activate the virtual environment.
3) Migrate: ``python manage.py migrate``.
4) Craete and fill hbms database: ``python create_db.py --user user_name --password password`` (Any user_name and password permitted to create a database in your server.)
5) Run app: ``python manage.py runserver``.
6) Open the host address (localhost by defaukt) on your preferred browser to access the HBMS application.

