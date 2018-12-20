##
#
# This class helps to use the Printful API
#
# version 1.0
# copyright 2014 Idea Bits LLC
#
##

import json
import urllib
import urllib2
import base64

class PrintfulClient:

    API_URL = 'https://api.theprintful.com/'
    USER_AGENT = 'Printful API Python Library 1.0'

    key = None
    last_response_raw = None
    last_response = None

    # Initialize API library
    # key - Printful Store API key
    def __init__(self, key):
        self.key = key

    # Returns total available item count from the last request if it supports paging (e.g order list) or nil otherwise
    def item_count(self):
        if(self.last_response and 'paging' in self.last_response):
            return self.last_response['paging']['total']
        else:
            None

    # Perform a GET request to the API
    # path - Request path (e.g. 'orders' or 'orders/123')
    # params - Additional GET parameters as a dictionary
    def get(self, path, params=None):
        return self.__request('GET', path, params)

    # Perform a DELETE request to the API
    # path - Request path (e.g. 'orders' or 'orders/123')
    # params - Additional GET parameters as a dictionary
    def delete(self, path, params=None):
        return self.__request('DELETE', path, params)

    # Perform a POST request to the API
    # path - Request path (e.g. 'orders' or 'orders/123')
    # data - Request body data as a dictionary
    # params - Additional GET parameters as a dictionary
    def post(self, path, data=None, params=None):
        return self.__request('POST', path, params, data)

    # Perform a PUT request to the API
    # path - Request path (e.g. 'orders' or 'orders/123')
    # data - Request body data as a dictionary
    # params - Additional GET parameters as a dictionary
    def put(self, path, data=None, params=None):
        return self.__request('PUT', path, params, data)

    # Internal generic request wrapper
    def __request(self, method, path, params=None, data=None):

        self.last_response = None
        self.last_response_raw = None

        opener = urllib2.build_opener(urllib2.HTTPSHandler())

        url = self.API_URL + path
        if(params):
            url += '?' + urllib.urlencode(params)

        if data:
            body = json.dumps(data)
        else:
            body = None

        request = urllib2.Request(url)
        request.get_method = lambda: method
        request.add_header("Authorization", "Basic %s" % base64.standard_b64encode(self.key))
        request.add_header('User-Agent', self.USER_AGENT)
        request.add_header('Content-Type', 'application/json')
        try:
            result = opener.open(request, body, 30)
        except urllib2.HTTPError as e:
            result = e
        except Exception as e:
            raise PrintfulException('API request failed: %s' % e)

        self.last_response_raw = output = result.read()

        try:
            data = json.loads(output)
            self.last_response = data
        except ValueError as e:
            raise PrintfulException('API response was not valid JSON')

        if(not('code' in data  and 'result' in data)):
            raise PrintfulException('Invalid API response')

        status = data['code']
        if(status<200 or status >=300):
            raise PrintfulApiException(data['result'], data['code'])

        return data['result']



# Generic Printful exception
class PrintfulException(Exception):
    pass

# Printful exception returned from the API
class PrintfulApiException(PrintfulException):
    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code
    def __str__(self):
        return '%i - %s' % (self.code, self.message)