from datetime import datetime

class DataNbaGameItem(object):
    """
    Class for game data from data.nba.com

    :param dict item: dict with game data
    """

    def __init__(self, item):
        self.game_id = int(item.get("gid"))
        self.date = item.get("gdte")
        self.utc_time = item.get("utctm")
        self.DateTimeUTC = datetime.strptime(f"{self.date} {self.utc_time}", "%Y-%m-%d %H:%M")
        self.status = item.get("stt")
        self.series_summary = item.get("seri")
        self.home_team_id = item.get("h", {}).get("tid")
        self.home_team_record = item.get("h", {}).get("re")
        self.home_team_abbreviation = item.get("h", {}).get("ta")
        self.home_team_name = item.get("h", {}).get("tn")
        self.home_team_city = item.get("h", {}).get("tc")
        self.home_score = int(item.get("h", {}).get("s", 0))
        self.away_team_id = item.get("v", {}).get("tid")
        self.away_team_record = item.get("v", {}).get("re")
        self.away_team_abbreviation = item.get("v", {}).get("ta")
        self.away_team_name = item.get("v", {}).get("tn")
        self.away_team_city = item.get("v", {}).get("tc")
        self.away_score = int(item.get("v", {}).get("s", 0))
        self.stadium = item.get("an")
        self.stadium_city = item.get("ac")
        self.stadium_state = item.get("as")

    @property
    def data(self):
        """
        returns game dict
        """
        return self.__dict__

    @property
    def is_final(self):
        """
        returns True if game is final, False otherwise
        """
        return self.status == "Final"
