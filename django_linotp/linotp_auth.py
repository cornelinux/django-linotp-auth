'''
Add the following to your project/settings.py

AUTHENTICATION_BACKENDS =  ('django_linotp.linotp_auth.LinOTP', )

LINOTP = { 'url' : 'https://puckel/validate/check',
        'timeout' : 5,
        'ssl_verify' : False,
        'host_verify' :  False,
	'create_user' : False,
        }


'create_user': if set to True, the user in the django DB will be created, if LinOTP returns a successful authentication

'''
from django.conf import settings
from django.contrib.auth.models import User, check_password

import sys
import pycurl
import logging
import traceback

from urllib import urlencode
import json

logger = logging.getLogger(__name__)

class Test:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf

class LinOTP(object):


    def __init__(self):
	self.url = 'https://localhost/validate/check'
	self.timeout = 5
	self.ssl_verify = False
	self.host_verify = False
	self.create_user = False
	if settings.LINOTP:
	    self.url = settings.LINOTP.get('url', self.url)
	    self.timeout = settings.LINOTP.get('timeout', self.timeout)
	    self.ssl_verify = settings.LINOTP.get('ssl_verify', self.ssl_verify)
	    self.host_verify = settings.LINOTP.get('host_verify', self.host_verify)
	    self.create_user = settings.LINOTP.get('create_user', self.create_user)

    def authenticate(self, username=None, password=None):
        user = None
	try:
	        t = Test()
	        c = pycurl.Curl()
		params = { 'user' : username, 'pass' : password }
		url = str("%s?%s"  %   (self.url, urlencode(params)))
		print "Connecting to %s" % url
	        c.setopt(c.URL, url)
	        c.setopt(c.WRITEFUNCTION, t.body_callback)
	        c.setopt(c.HEADER, False)
	        c.setopt(c.SSL_VERIFYPEER, self.ssl_verify)
	        c.setopt(c.SSL_VERIFYHOST, self.host_verify)
	        c.setopt(c.CONNECTTIMEOUT, self.timeout)
	        c.perform()
	        c.close()             	   
		print t.contents
		res = json.loads(t.contents)
		if (res.get('result',{}).get('status') == True and 
			res.get('result',{}).get('value') == True):
		    user = User.objects.get(username=username)
	
	except User.DoesNotExist:
	    # The user was authenticated by LinOTP but does not exist!
	    print "User authenticated but does not exist"
	    if self.create_user:
		print "creating user"
		# FIXME: For any reason does not work at the moment
		user = User(username=username, password="supersecret")	
		user.is_staff = True
		user.is_superuser = False
		user.save

        except Exception as e:
	    print traceback.format_exc()		
	    print e

	return user

    def get_user(self, user_id):
	try:
            return User.objects.get(pk=user_id)
	except User.DoesNotExist:
	    return None

