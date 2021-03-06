import json
# import urllib
import urllib.request as urllib2
from urllib.parse import urljoin
from urllib.parse import urlencode

class Http(object):
  def __init__(self, version, url, debug=False):
    self.version = version
    self.url = url
    self._debug = debug

  def _call_server(self, url, post_data):
    if not url:
      response = dict(error=True, message='AttributeError: Bad URL: ' + str(url))
      return json.dumps(response)
    data = urlencode(post_data).encode("utf-8")
    request = urllib2.Request(url, data)
    #print('call_server: ', url, data)
    try:
      res = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
      headers = e.headers if self._debug else ''
      response = dict(error=True, message='HTTPError: {0} {1} {2}'.format(e.code, e.reason, headers))
      response = json.dumps(response)
    except urllib2.URLError as e:
      response = dict(error=True, message='URLError: {0}'.format(e.reason))
      response = json.dumps(response)
    except BaseException as e:
      response = dict(error=True, message='Error: {0}'.format(e))
      response = json.dumps(response)
    else:
      res2 = res.read()
      response = res2 if isinstance(res2, str) else res2.decode('utf-8')      
    return response

  def request(self, api_name, data):
    path = '{version}/{api_name}'.format(version=self.version, api_name=api_name)
    response = self._call_server(urljoin(self.url, path), data)
    try:
      response = json.loads(response)
    except ValueError as e:
      response = dict(error=True, message=repr(e))
    return response

  def post(self, url, data):
    response = self._call_server(url, data)
    try:
      response = json.loads(response)
    except ValueError as e:
      response = dict(error=True, message=repr(e))
    return response
