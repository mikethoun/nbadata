import requests

from pbpstats import NBA_STRING, D_LEAGUE_STRING, WNBA_STRING
from pbpstats.data_loader.abs_data_loader import AbsDataLoader


class DataNbaWebLoader(AbsDataLoader):
    """
    base class for loading data from data.nba.com
    should not be called directly
    """
    def _load_request_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.source_data = response.json()
            self._save_data_to_file()
        else:
            response.raise_for_status()

    @property
    def league(self):
        """
        First 2 in game id represent league
        00 for nba, 10 for wnba, 20 for g-league
        """
        if self.game_id[0:2] == '00':
            return NBA_STRING
        elif self.game_id[0:2] == '20':
            return D_LEAGUE_STRING  # url uses dleague instead of gleague
        elif self.game_id[0:2] == '10':
            return WNBA_STRING

    @property
    def season(self):
        """
        season url part is year in which season starts
        4th and 5th characters in game id represent season year
        ex. for 2016-17 season 4th and 5th characters would be 16 and season should return 2016
        """
        if self.game_id[3] == '9':
            return '19' + self.game_id[3] + self.game_id[4]
        else:
            return '20' + self.game_id[3] + self.game_id[4]
