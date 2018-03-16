class Team:
    def __init__(self, team_info):
        self.name = ''
        for key, value in team_info.items():
            setattr(self, key, value)

    def __repr__(self):
        return self.name

    def save(self):
        self_data = {}
        for key, value in vars(self).items():
            self_data[key] = value
        return self_data
