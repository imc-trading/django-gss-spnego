FROM debian:jessie

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -qq update
RUN apt-get -qq install apt-transport-https locales krb5-user curl
RUN apt-get -qq clean

COPY krb5.conf /etc/
COPY kerberos-client/run.sh kerberos-client/wait-for-it.sh /tmp/

CMD ["/tmp/run.sh"]