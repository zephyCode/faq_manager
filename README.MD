# FAQ_Manger assignment solution BHARAT FD

- Step I: Enviroment setup and project creation using the command
    "django-admin startproject faq_manager"

- Step II: Creation of models.py file inside the faq_manager folder

- Step III: admin.py file is created for giving the admin control to manage the faqs in the app.

- Step IV: fixing of migrations are done in this commit as well. Using the commands. **python manage.py makemigrations**, **python manage.py migrate**

- Step V: views.py and serializers.py file is created for **Django REST Api framework** and also urls.py file is modified

- Step VI: **Djando Rest Framework** is installed using the command **pip install djangorestframework**

- Step VII: **settings.py** is modified

- Step VIII: **apps.py** file is created

- Step IX: **urls.py** file is modified

- Step X: Installed the ckeditor using the command **pip install django-ckeditor** and also **settings.py** is modified

- Step XI: Implementation of the cache and google trans in the **models.py** file

- Step XII: **serializers.py**, **admin.py**, **settings.py**, **urls.py**, **views.py** are modified for cache and admin portal to manage faqs.

- Step XIII: An error encounterd for table **faq_manager_faq table is not found** so i fixed that with following commands. **python manage.py makemigrations faq_manager** and also verified the **INSTALLED_APPS** field in the **settings.py** file.


