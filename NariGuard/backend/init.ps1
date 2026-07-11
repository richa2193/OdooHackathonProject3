python -m venv venv
.\venv\Scripts\activate
pip install django djangorestframework django-cors-headers psycopg2-binary python-dotenv requests google-generativeai cloudinary
django-admin startproject config .
python manage.py startapp core
python manage.py startapp api
