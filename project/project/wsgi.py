import os, sys, site
from os.path import abspath, dirname
from sys import path

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.append(SITE_ROOT)


# Tell wsgi to add the Python site-packages to its path. 
site.addsitedir('/home/grupodms/.virtualenvs/puntodeventa_demo/lib/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.produccion")

activate_this = os.path.expanduser("~/.virtualenvs/puntodeventa_demo/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/grupodms/webapps/puntodeventa_demo/project/project/'
workspace = os.path.dirname(project)
sys.path.append(workspace)


from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()