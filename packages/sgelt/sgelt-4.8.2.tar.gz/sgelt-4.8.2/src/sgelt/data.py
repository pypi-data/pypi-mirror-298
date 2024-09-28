"""
A module to store agenda, news, events and teams data
To be populated and modified by sgelt module
"""

from .utils import read_data


class Data:
    """A class to store site data"""

    def __init__(self, conf):
        """Initialize with configuration object and empty data"""

        self.conf = conf  # a configuration object
        # read from agenda.json
        self.conferences = []
        self.defenses = []
        self.seminars = []

        self.teams = {}  # read from teams.json

        self.news = []  # will be populated by registering news
        self.libnews = []  # will be populated by registering libnews
        self.events = []  # will be populated by registering events

    def read_files(self):
        """Read data from json files"""

        # Read agenda data from json file
        agenda = read_data(self.conf.json_agenda_path)
        self.conferences = agenda['conferences']
        self.defenses = agenda['defenses']
        self.seminars = agenda['seminars']

        # Read team data from json file
        self.teams = read_data(self.conf.json_teams_path)

    def __repr__(self):
        from pprint import pformat
        return '\n'.join((f"{k}: {pformat(v)}"
                          for k, v in vars(self).items()))
