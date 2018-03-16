from ncaa.game import Game
from ncaa.team import Team


class Region:
    def __init__(self, region_name):
        self.games = []
        self.region_name = region_name

    def add_game(self, game_info):
        game = Game()
        game.scrape_load(game_info, self.region_name)
        self.games.append(game)

    def load(self, region):
        # pprint.pprint(region)
        for team, info in region.items():
            game = Game()
            game.load(info)
            self.games.append(game)

    def save(self):
        game_info = []
        for game in self.games:
            game_info.append(game.save())
        return game_info
