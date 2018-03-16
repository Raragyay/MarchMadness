from ncaa.team import Team


class Region:
    def __init__(self):
        self.teams = []

    def add_team(self, team):
        self.teams.append(team)

    def load(self, region):
        # pprint.pprint(region)
        for team, info in region.items():
            self.teams.append(Team(kwargs=info))

    def save(self):
        team_info = {}
        for team in self.teams:
            team_info[team.name] = team.save()
        return team_info
