#!/bin/bash
if [ ! -f /tmp/user.keytab ]; then
    kadmin -p admin -w admin -q "ktadd -k /tmp/user.keytab admin@EXAMPLE.COM"
fi
kinit -kt /tmp/user.keytab admin

/tmp/wait-for-it.sh django-gss-spnego:8003
curl -L -c /tmp/cookies.txt -vv --negotiate -u : http://django-gss-spnego:8003/auth/spnego | grep -q "admin/logout"
