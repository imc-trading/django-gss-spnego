#!/bin/bash
if [ ! -f /tmp/user.keytab ]; then
    kadmin -p admin -w admin -q "ktadd -k /tmp/user.keytab admin@EXAMPLE.COM"