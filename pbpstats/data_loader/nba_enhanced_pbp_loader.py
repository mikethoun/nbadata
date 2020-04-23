import os
import json
from collections import defaultdict

from pbpstats.overrides import IntDecoder
from pbpstats.resources.enhanced_pbp.start_of_period import StartOfPeriod
from pbpstats.resources.enhanced_pbp.foul import Foul


class NbaEnhancedPbpLoader(object):
    """
    class for shared methods between data and stats nba pbp loaders
    both DataNbaEnhancedPbpLoader and StatsNbaEnhancedPbpLoader should inherit this
    """
    def _add_extra_attrs_to_all_events(self):
        start_period_indices = []
        self._load_possession_changing_event_overrides()
        change_override_event_nums = self.possession_changing_event_overrides.get(self.game_id, [])
        non_change_override_event_nums = self.non_possession_changing_event_overrides.get(self.game_id, [])
        player_game_fouls = defaultdict(int)
        team_period_fouls = defaultdict(int)
        for i, event in enumerate(self.items):
            if i == 0 and i == len(self.items) - 1:
                event.previous_event = None
                event.next_event = None
            elif isinstance(event, StartOfPeriod) or i == 0:
                event.previous_event = None
                event.next_event = self.items[i + 1]
                start_period_indices.append(i)
                team_period_fouls = defaultdict(int)
            elif i == len(self.items) - 1 or event.period != self.items[i + 1].period:
                event.previous_event = self.items[i - 1]
                event.next_event = None
            else:
                event.previous_event = self.items[i - 1]
                event.next_event = self.items[i + 1]
            if isinstance(event, Foul):
                if event.counts_towards_penalty:
                    team_period_fouls[event.team_id] += 1
                if event.counts_as_personal_foul:
                    player_game_fouls[event.player1_id] += 1
            event.team_period_fouls = team_period_fouls.copy()
            event.player_game_fouls = player_game_fouls.copy()
            event.possession_changing_override = event.event_num in change_override_event_nums
            event.non_possession_changing_override = event.event_num in non_change_override_event_nums
        # these need next and previous event to be added to all events
        for i in start_period_indices:
            team_id = self.items[i].get_team_starting_with_ball()
            self.items[i].team_starting_with_ball = team_id
            period_starters = self.items[i].get_period_starters(file_directory=self.file_directory)
            self.items[i].period_starters = period_starters

    def _load_possession_changing_event_overrides(self):
        if self.file_directory is not None:
            possession_changing_event_overrides_file_path = f'{self.file_directory}/overrides/possession_change_event_overrides.json'
            if os.path.isfile(possession_changing_event_overrides_file_path):
                with open(possession_changing_event_overrides_file_path) as f:
                    # issues with pbp - force these events to be possession changing events
                    # {GameId: [EventNum]}
                    self.possession_changing_event_overrides = json.loads(f.read(), cls=IntDecoder)
            else:
                self.possession_changing_event_overrides = {}

            non_possession_changing_event_overrides_file_path = f'{self.file_directory}/overrides/non_possession_changing_event_overrides.json'
            if os.path.isfile(non_possession_changing_event_overrides_file_path):
                with open(non_possession_changing_event_overrides_file_path) as f:
                    # issues with pbp - force these events to be not possession changing events
                    # {GameId: [EventNum]}
                    self.non_possession_changing_event_overrides = json.loads(f.read(), cls=IntDecoder)
            else:
                self.non_possession_changing_event_overrides = {}
        else:
            self.possession_changing_event_overrides = {}
            self.non_possession_changing_event_overrides = {}
