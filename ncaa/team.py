class Team:
    def __init__(self, **kwargs):
        for key, value in kwargs['kwargs'].items():
            setattr(self, key, value)

    def save(self):
        self_data = {}
        for key, value in vars(self).items():
            self_data[key] = value
        return self_data
