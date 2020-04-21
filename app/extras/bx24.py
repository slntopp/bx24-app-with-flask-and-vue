import requests
import json

from typing import Union

class BX24:
    def __init__(self, portal: list):
        self.domain, self.token = portal


    def call(self, method: str, params: list = []) -> tuple:
        """ BX24.callMethod analog, returns status code and response.json as tuple
        :param method: method name as string, e.g. crm.lead.get
    
        :param params: params as list of tuples, e.g. [('ID', '42')]
    
        :rtype: tuple
        """
        response = requests.get(
            "https://%s/rest/%s/" % (self.domain, method),
            params=[('access_token', self.token)] + params
        )
        return response.status_code, response.json

    def check_auth(self):
        if self.call('app.info')[0] == 401:
            raise BX24.NoAuth
        return True

    def batch(self, params: Union[list, dict]):
        if type(params) == list:
            params = {
                i : params[i] for i in range(len(params))
            }

        keys = list(params.keys())
        for k in keys:
            params[k][1] = self.__format_params__(params[k][1])
            params["cmd[%s]" % k] = "{0}?{1}".format(*params[k])
            del params[k]

        params = [(k, v) for k, v in params.items()] 
        
        response = requests.post(
            "https://%s/rest/batch.json" % self.domain,
            params=[('access_token', self.token)] + params
        )
        return [response.status_code, response.text]

    def __format_params__(self, d: dict) -> str:
        result = []
        for k in d.keys():
            if type(d[k]) == dict:
                result.append(
                    self.__format_inner__(k, d[k])
                )
            else:
                result.append(
                    "%s=%s" % (k, d[k])
                )
        return '&'.join(result)

    def __format_inner__(self, pk: Union[str, int], d: dict) -> str:
        result = []
        for k in d.keys():
            if type(d[k]) == dict:
                d[k] = json.dumps(d[k])
            result.append(
                "%s[%s]=%s" % (pk, k, d[k])
            )
        return '&'.join(result)

    class NoAuth(Exception):
        pass

class Event:
    handler = 'https://%s/'

    def __init__(self, client: BX24, event: str = None):
        self.client = client
        self.event  = event

    def set_host(self, host):
        self.host = host
        return self
    
    def bind(self, uri: str = 'hook'):
        params = [
            'event.bind',
            [
                ('event', self.event),
                ('handler', (Event.handler % self.host) + uri)
            ]
        ]
        return self.client.call(*params)
    
    def list(self, scope: str = None):
        return self.client.call(
            'events', [
                ('scope', scope)
            ]
        )

class CRMInstance:
    def __init__(self, client, type):
        self.client = client
        self.type   = type