=================
django-gss-spngeo
=================

A Django application for adding Kerberos/GSS authentication to your existing backend

This Django application provides some ``View`` and ``Mixin`` classes along with a backend
``Mixin`` class to extend your existing ``AuthenticationBackend`` with SPNEGO-based authentication.

Prereqs
-------
* A working Kerberos KDC (MIT, Windows AD, Heimdall, whatever)
* A SPN for your application server(s)
* A method for mapping Kerberos Principals to User objects in your backend

Configuration
-------------
The following settings must be present:

* ``django_gss_spnego`` in ``settings.INSTALLED_APPS``
* ``settings.KERBEROS_SPN`` may be set to ``SERVICENAME@HOSTNAME`` `ie` ``HTTP@django-server``.
  Setting it to "" means "try all SPNs in the host keytab"
* Environment variables to control your KRB5 installation.
  See the `kerberos env`_ documentation for details.

Usage
-----
Mix ``django_gss_spnego.backends.SpnegoBackendMixin`` into your backend class(es) of choice.
Ensure those backends can resolve a User object from a kerberos principal name.

.. code-block:: python

    from django_auth_ldap.backend import LDAPBackend
    from django_gss_spnego.backends import SpnegoBackendMixin


    class MyBackendClass(SpnegoBackendMixin, LDAPBackend):
        def get_user_from_username(self, username):
            return self.populate_user(username)

Register aforementioned backend class in ``settings.AUTHENTICATION_BACKENDS``

Create a view somewhere on your site that uses ``SpnegoAuthMixin``, and add it to your URL router.
If using one of the provided CBV View classes, also include ``django_gss_spnego`` and
``django.contrib.admin`` in your ``settings.INSTALLED_APPS`` for access to the spnego.html template.

.. code-block:: python

    from django_gss_spnego.views import SpnegoView

    urls.append(r"^auth/spnego$", SpnegoView.as_view(), name="spnego")

Acquire a ticket, and point your favorite supported client at the endpoint

.. code-block:: python

    import requests_gssapi
    import requests

    auth = requests_gssapi.HTTPSPNEGOAuth()
    sess = requests.session()
    sess.auth = auth
    sess.get("http://localhost/auth/spnego")
    sess.get("http://localhost/page/that/requires/authorized_user")

Acknowledgements
----------------
* `Matt Magin (AzMoo)`_ for writing a `similar Middleware`_


License
-------
Apache 2.0 -- see the LICENSE file for more detail

.. _Matt Magin (AzMoo): https://github.com/AzMoo
.. _similar Middleware: https://github.com/AzMoo/django-auth-spnego
.. _kerberos env: http://web.mit.edu/kerberos/www/krb5-1.16/doc/user/user_config/kerberos.html#kerberos-7
