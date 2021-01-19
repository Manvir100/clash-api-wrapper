import requests


class _Api:

    def __init__(self, player_region, api_key):
        self._player_region = player_region
        self._api_key = api_key

    @staticmethod
    def _get_data(url):
        response = requests.get(url)
        return response.json()


class Team(_Api):

    def __init__(self, player_name, player_region, api_key):
        super(Team, self).__init__(player_region, api_key)
        self._summoner_id = self._get_summoner_id(player_name)
        self._team_id = self._get_team_id()
        self._team_data = self._get_team_data()
        self._player_data = self._get_player_data()
        self.team_mates = self._get_players()
        self.tournament = self._get_tournament()

    def _get_summoner_id(self, player_name):
        try:
            return self._get_data("https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
                                  .format(self._player_region, player_name, self._api_key))['id']
        except():
            raise Exception("Summoner not found")

    def _get_team_id(self):
        try:
            return self._get_data("https://{}.api.riotgames.com/lol/clash/v1/players/by-summoner/{}?api_key={}"
                                  .format(self._player_region, self._summoner_id, self._api_key))[0]['teamId']
        except():
            raise Exception("Summoner is not on a clash team")

    def _get_team_data(self):
        try:
            return self._get_data("https://{}.api.riotgames.com/lol/clash/v1/teams/{}?api_key={}"
                                  .format(self._player_region, self._team_id, self._api_key))
        except():
            raise Exception("Team data not found")

    def _get_player_data(self):
        try:
            return self._team_data['players']
        except():
            raise Exception("Players data not found")

    def _get_players(self):
        players = []
        for player in self._player_data:
            players.append(_Player(player, self._player_region, self._api_key))
        return players

    def _get_tournament(self):
        return _Tournament(self._team_data['tournamentId'], self._player_region, self._api_key)

    @property
    def name(self):
        return self._team_data['name']

    @property
    def icon_id(self):
        return self._team_data['iconId']

    @property
    def tier(self):
        return self._team_data['tier']

    @property
    def abbreviation(self):
        return self._team_data['abbreviation']


class _Tournament(_Api):

    def __init__(self, tournament_id, player_region, api_key):
        super(_Tournament, self).__init__(player_region, api_key)
        self._tournament_id = tournament_id
        self._tournament_data = self._get_tournament_data()

    def _get_tournament_data(self):
        try:
            return self._get_data("https://{}.api.riotgames.com/lol/clash/v1/tournaments/{}?api_key={}"
                                  .format(self._player_region, self._tournament_id, self._api_key))
        except():
            raise Exception("Tournament data not found")

    @property
    def name(self):
        return self._tournament_data['nameKey']

    @property
    def name_secondary(self):
        return self._tournament_data['nameKeySecondary']


class _Player(_Api):

    def __init__(self, player, player_region, api_key):
        super(_Player, self).__init__(player_region, api_key)
        self._player_data1 = player
        self._player_data2 = self._get_player_data()

    def _get_player_data(self):
        try:
            data = self._get_data("https://{}.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}"
                                  .format(self._player_region, self._player_data1['summonerId'], self._api_key))
            if data[0]['queueType'] == "RANKED_SOLO_5x5":
                data = data[0]
            else:
                try:
                    data = data[1]
                except():
                    data = data[0]
            return data
        except():
            raise Exception("Player data not found")

    @property
    def name(self):
        return self._player_data2['summonerName']

    @property
    def tier(self):
        return self._player_data2['tier']

    @property
    def rank(self):
        return self._player_data2['rank']

    @property
    def position(self):
        return self._player_data1['position']

    @property
    def role(self):
        return self._player_data1['role']