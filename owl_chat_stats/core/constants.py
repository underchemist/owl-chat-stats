from datetime import date
from model_utils import Choices


class ReversibleChoices(Choices):
    def _human_to_db(self, value):
        """Get the database representation of a choice from the human readable representation"""
        mapping = self._display_map.copy()
        for db, human in mapping.items():
            if value == human:
                return db
        raise KeyError(f"{value} not found")


TEAMS = ReversibleChoices(
    ("sfshock", ("San Francisco Shock")),
    ("vtitans", ("Vancouver Titans")),
    ("nyexcelsior", ("New York Excelsior")),
    ("hspark", ("Hangzhou Spark")),
    ("lagladiators", ("Los Angeles Gladiators")),
    ("areign", ("Atlanta Reign")),
    ("lspitfire", ("London Spitfire")),
    ("gcharge", ("Guangzhou Charge")),
    ("pfusion", ("Philadelphia Fusion")),
    ("sdynasty", ("Seoul Dynasty")),
    ("sdragons", ("Shanghai Dragons")),
    ("chunters", ("Chengdu Hunters")),
    ("lavaliant", ("Los Angeles Valiant")),
    ("peternal", ("Paris Eternal")),
    ("dfuel", ("Dallas Fuel")),
    ("houtlaws", ("Houston Outlaws")),
    ("tdefiant", ("Toronto Defiant")),
    ("wjustice", ("Washington Justice")),
    ("buprising", ("Boston Uprising")),
    ("fmayhem", ("Florida Mayhem")),
)

SEASONS = (1, 2)

SEASONS_YEAR_MAP = {2018: 1, 2019: 2}
