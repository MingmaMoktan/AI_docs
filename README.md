# AI Docs — MVP

Django app to generate documentation from code/sql zips.

## Run locally (WSL)
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. export DJANGO_SECRET_KEY="change-me"
5. python manage.py migrate
6. python manage.py runserver
