from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import EndOfPeriod


class StatsEndOfPeriod(EndOfPeriod, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)