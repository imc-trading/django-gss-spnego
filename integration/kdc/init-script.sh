echo "==== Creating realm ==============================================================="
MASTER_PASSWORD=$(tr -cd '[:alnum:]' < /dev/urandom | fold -w30 | head -n1)
# This command also starts the krb5-kdc and krb5-admin-server services
krb5_newrealm <<EOF
$MASTER_PASSWORD
$MASTER_PASSWORD
EOF
echo ""

echo "==== Creating the principals in the acl ==========================================="
echo "Adding admin principal"
kadmin.local -q "delete_principal -force admin@EXAMPLE.COM"
echo ""
kadmin.local -q "addprinc -pw admin admin@EXAMPLE.COM"
echo ""

echo "Adding HOST principal"
kadmin.local -q "delete_principal -force HOST/django-gss-spnego@EXAMPLE.COM"
echo ""
kadmin.local -q "addprinc -pw django-gss-spnego HOST/django-gss-spnego@EXAMPLE.COM"
echo ""

echo "Adding HTTP principal"
kadmin.local -q "addprinc -randkey HTTP/django-gss-spnego@EXAMPLE.COM"
