import httplib2

from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLOW = OAuth2WebServerFlow(
	# Client id, secret from http://code.google.com/apis/console#access
    client_id='146153464872.apps.googleusercontent.com',
    client_secret='iiZSwCtCMqCIPYWltpprxY41',
    scope='https://www.googleapis.com/auth/taskqueue',
    user_agent='python-gae-queues-demo/1.0')

# If the Credentials don't exist or are invalid run through the native client
# flow. The Storage object will ensure that if successful the good Credentials
# will get written back to a file.
storage = Storage('credentials.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
	credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)
