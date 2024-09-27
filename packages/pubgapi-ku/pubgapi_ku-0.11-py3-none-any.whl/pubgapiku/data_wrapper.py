"""Wrap response data into other data types which are easy to handle"""
import pandas as pd
from api_connector import Connector

class DataWrapper():
    """Data wrapper class"""
    def __init__(self, api_key:str, timeout:int):
        self.conn = Connector(api_key, timeout)

    def get_sample_matches(self) -> list|None:
        """
        Get a list of random sample match

        [Return]
        list |-> Successfully extracted matchid list
        None |-> Fail signal
        """

        data:dict|None = self.conn.sample_matches()
        if isinstance(data, dict):
            match_list:list = [
                item['id'] for item in
                data['data']['relationships']['matches']['data']
            ]
            return match_list
        else:
            return None

    def get_players_in_match(self, match_id:str) -> pd.DataFrame|None:
        """
        Get a dataframe containing player names and account ids of a matchß

        [Return]
        pd.DataFrame |-> Successfully extracted player info
        None         |-> Fail signal
        """

        data:dict|None = self.conn.match(match_id)
        if isinstance(data, dict):
            player_list:list = [
                {'accountId': item['attributes']['stats']['playerId'],
                 'playerName': item['attributes']['stats']['name']}
                for item in data['included']
                if item['type'] == 'participant'
            ]
            return pd.DataFrame(player_list)
        else:
            return None

    def get_player_data(self, **kargs):
        """
        Get a dataframe containing matches and corresponding players to each match

        [Keyword arguments]
        ids:list[str]   |-> filters by player IDs
        names:list[str] |-> filters by player names

        [Return]
        pd.DataFrame |-> Successfully extracted player-match relations
        None         |-> Fail signal
        """

        data:dict|None = self.conn.players(**kargs)
        if isinstance(data, dict):
            player_datas = []
            for player in data['data']:
                player_id = player['id']
                player_name = player['attributes']['name']
                player_bantype = player['attributes']['banType']

                for match in player['relationships']['matches']['data']:
                    if match['type'] == 'match':
                        match_info = {
                            'accountId': player_id,
                            'playerName': player_name,
                            'banType': player_bantype,
                            'matchId': match['id']
                        }
                        player_datas.append(match_info)
            return pd.DataFrame(player_datas)
        else:
            return None

    def get_match_data(self, match_id:str) -> tuple[dict, dict]|None:
        """
        Get a dataframe containing a match's metadata and the address of telemetry file

        [Argument]
        match_id:str |-> target match's id

        [Return]
        tuple[dict, dict] |-> Successfully acquired match and telemetry data
        None              |-> Fail signal
        """

        match_data:dict|None = self.conn.match(match_id)
        if isinstance(match_data, dict):
            telemetry_addr:str|None = self.conn.telemetry_addr(match_data)
            if not isinstance(telemetry_addr, str):
                return None

            telemetry_data:dict|None = self.conn.get_telemetry(telemetry_addr)
            if not isinstance(telemetry_data, dict):
                return None
            else:
                return match_data, telemetry_data
        else:
            return None
