"""
WSGI config for Treemap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
path = '/var/www/Treemap/'
if path not in sys.path:
	sys.path.append(path)
sys.path.insert(1,'/usr/local/lib/python3.6/dist-packages')
filepath='/var/log/apache2/output2.txt'
with open(filepath,'w') as f:
	f.write('sys.path:'+str(sys.path))
f.close()

from django.core.wsgi import get_wsgi_application,WSGIHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Treemap.settings')

application = get_wsgi_application()
