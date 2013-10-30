django-linotp-auth
==================

two factor authentication with LinOTP for django and djangoCMS.

configure
---------

In your projetc/settings.py add this as authentication module::
   
   AUTHENTICATION_BACKENDS =  ('django_linotp.linotp_auth.LinOTP', )

Then you can add a dictionary LINOTP with all necessary configuration::
   
   LINOTP = { 'url' : 'https://puckel/validate/check',
        'timeout' : 5,
        'ssl_verify' : False,
        'host_verify' :  False,
        'create_user' : False,
        }

The url contains the location of your LinOTP server.
If you have no trusted SSL certificate you should set
ssl_verify and host_verify to False.

create_user is not working at the moment.
You need to create the user in django manually. The user
also needs to exist in the corresponding LinOTP UserIdResolver.

See: https://docs.djangoproject.com/en/dev/topics/auth/customizing/
