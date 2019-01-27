#!/bin/bash

if [ ! -f /etc/krb5.keytab ]; then
    kadmin -p HOST/django-gss-spnego -w django-gss-spnego -q "ktadd -k /etc/krb5.keytab -glob *django-gss-spnego*"
fi
cd /srv/

python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')" | python manage.py shell
python manage.py runserver 0.0.0.0:8003