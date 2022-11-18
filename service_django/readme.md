#enter django container
docker exec -it django /bin/bash

python manage.py makemigrations
python manage.py migrate

#建立專案
django-admin startproject phantom_mask

#SECRET_KEY generate
https://djecrety.ir/

#create superuser
python manage.py createsuperuser

