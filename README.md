###1. Get clone of the Project

###2. Install all the requirements
    pip install -r requirements.txt
    
###3. Create new database in postgresql
    sudo-i -u postgres
    psql
    create database advarisk_news;
    \q
    exit

###4. Change database password and user in settings.py

###5. Migratations
    python manage.py makemigrations admin_panel customer
    python manage.py migrate

###6. Create superuser
    python manage.py createsuperuser

###7. Login with superuser:
_After login with superuser you can see:_
    1.  Dashboard
    2.  User's list
    3.  Create New User

###8. Login with user:
_After login with user you can see:_
    1.  Search news with keyword or phrase
    2.  See the original news in new tab
