import requests
import json

class Helper:

    @staticmethod
    def make_query(url, header, params=None):
        """ Make a query to the url
        Params:
            - url (string). This is the url that will be requested.
            - header (dict). This is the header to send to the request.

        Functionality:
            - Make a query GET query to the url.
            If status_code is 200,return the text request.
            If status_cose is diferent, raise an Exception.

        Returns:
            - Return a 'dict' (json) object.
            - Returns an error because the url is malformed.
        """
        if params != None:
            response = requests.get(url, headers=header, params=params)
        else:   
            response = requests.get(url, headers=header)
            
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception("Bad request for this url", url)
