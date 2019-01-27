FROM debian:jessie

EXPOSE 749 88

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -qq update
RUN apt-get -qq install locales krb5-kdc krb5-admin-server
RUN apt-get -qq clean

COPY krb5.conf /etc/
COPY kdc/kdc.conf kdc/kadm5.acl /etc/krb5kdc/

COPY kdc/init-script.sh kdc/run.sh /tmp/
RUN /tmp/init-script.sh

CMD ["/tmp/run.sh"]