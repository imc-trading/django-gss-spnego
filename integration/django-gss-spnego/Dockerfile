FROM django-gss-spnego:dev

EXPOSE 8003

COPY ./django-gss-spnego /srv

WORKDIR /srv

COPY krb5.conf /etc/

CMD ["/srv/run.sh"]