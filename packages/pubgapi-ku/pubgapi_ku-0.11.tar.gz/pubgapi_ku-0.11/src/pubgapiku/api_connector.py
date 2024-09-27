"""KRAFTON API Request sender"""
import requests

class Connector:
    """API Request sender class"""
    def __init__(self, api_key:str, timeout:int):
        self.timeout:int = timeout
        self.api_base:str = "https://api.pubg.com/shards/steam/"
        self.header:dict = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/vnd.api+json'
        }
        self.header_nokey:dict = {
            'Accept': 'application/vnd.api+json'
        }
        self.err_stats = (401, 404, 415, 429)

    def err_check(self, response:requests.Response) -> dict|None:
        """
        Check the status code of the response and return None or Dictionarized response

        [Arguments]
        response:requests.Response |-> target response to check

        [Return]
        dict |-> When the status code of the response is 200
        None |-> When the response status code is one of the elements of <self.err_stats> tuple
        """
        if response.status_code in self.err_stats:
            return None
        else:
            return response.json()

    def sample_matches(self) -> dict|None:
        """Get sample match list"""
        api = self.api_base + '/samples'
        response:requests.Response = requests.get(api, headers=self.header, timeout=self.timeout)
        return self.err_check(response)

    def players(self, **kargs) -> dict|None:
        """
        Get players information

        [Keyword arguments]
        ids:list[str]   |-> filters by player IDs
        names:list[str] |-> filters by player names

        [Return]
        dict |-> When it gets a proper response from the request
        None |-> Whenever it gets an error, improper response or wrong input keyword arguments
        """

        fil_by_id:bool = ('ids' in kargs) and (len(kargs['ids']) > 0)
        fil_by_name:bool = ('names' in kargs) and (len(kargs['ids']) > 0)

        assert fil_by_id or fil_by_name, 'You have to use one of filters'
        assert not (fil_by_id and fil_by_name), 'You cannot use both filters at the same time'

        if fil_by_id:
            filter_:str = 'playerIds'
            filter_elements:str = ','.join(kargs['ids'])
        elif fil_by_name:
            filter_:str = 'playerNames'
            filter_elements:str = ','.join(kargs['names'])
        else:
            return None

        api:str = self.api_base + f'/players?filter[{filter_}]={filter_elements}'
        response:requests.Response = requests.get(api, headers=self.header, timeout=self.timeout)
        return self.err_check(response)

    def match(self, match_id:str) -> dict|None:
        """
        Get a match's information

        [Argument]
        match_id:str |-> target match's ID

        [Return]
        dict |-> When it gets a proper response from the request
        None |-> Whenever it gets an error, improper response
        """
        api = self.api_base + f'/matches/{match_id}'
        response:requests.Response = requests.get(
            api, headers=self.header_nokey, timeout=self.timeout
        )
        return self.err_check(response)

    def telemetry_addr(self, match_data:dict) -> str|None:
        """
        Get the address of telemetry data from a match data

        [Argument]
        match_data:dict |-> A match data which is obtained through the match function

        [Return]
        str |-> The address of the match's telemetry data
        """
        included:list[dict] = match_data['included']
        for item in included:
            if item['type'] == 'asset':
                return item['attributes']['URL']
        return None

    def get_telemetry(self, addr:str) -> dict|None:
        """
        Get telemetry data of a match

        [Argument]
        addr:str |-> The address of the telemetry data

        [Return]
        str |-> The address of the match's telemetry data
        """
        response:requests.Response = requests.get(
            addr, headers=self.header_nokey, timeout=self.timeout
        )
        return self.err_check(response)
