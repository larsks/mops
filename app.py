#!/usr/bin/env python
import imp
import os
import logging

try:
   zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                           'virtenv', 'bin', 'activate_this.py')
   exec(compile(open(zvirtenv).read(), zvirtenv, 'exec'),
        dict(__file__ = zvirtenv) )
except IOError:
   pass

def run_simple_httpd_server(app, ip, port=8080):
   from wsgiref.simple_server import make_server
   make_server(ip, port, app).serve_forever()

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

import bottle
import mops

#
#  main():
#
if __name__ == '__main__':
   ip   = os.environ['OPENSHIFT_PYTHON_IP']
   port = int(os.environ['OPENSHIFT_PYTHON_PORT'])

   logging.basicConfig(
           level = logging.DEBUG,
           format='%(asctime)s %(name)s/%(levelname)s: %(message)s',
           datefmt='%Y-%m-%d %H:%M:%S')

   mops.setup()
   bottle.run(mops.app, host=ip, port=port)

