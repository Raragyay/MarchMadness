from jsoninterchange import loader, dumper
from ncaa.region import Region
from ncaa.team import Team
from urlconnection import soupify


class Bracket:
    def __init__(self, round_num):
        self.region_0 = Region('First Four')
        self.region_1 = Region('South')
        self.region_2 = Region('East')
        self.region_3 = Region('West')
        self.region_4 = Region('Mid-West')
        self.region_dict = {
            0: self.region_0,
            1: self.region_1,
            2: self.region_2,
            3: self.region_3,
            4: self.region_4
        }

        self.region_names = {
            0: 'First Four',
            1: 'South',
            2: 'East',
            3: 'West',
            4: 'Mid-West'
        }
        self.round_num = round_num

    def load_team_stats(self):
        regions = loader('teamstats')
        # pprint.pprint(regions)
        if regions:
            for region_num, region in regions.items():
                region_num = int(region_num)
                self.region_dict[region_num].load(region)
        else:
            self.scrape_names()

    def save_team_stats(self):
        regions = {}
        for region_num, region in self.region_dict.items():
            regions[region_num] = region.save()
        dumper(regions, 'teamstats')

    def scrape_names(self):
        soup = soupify('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men')
        for region_num, region in enumerate(soup.find_all('li', class_=f'round{self.round_num}', limit=5)):
            print(region_num)
            for game in region.find_all('li', class_='game'):
                self.region_dict[region_num].add_game(
                        game)


b = Bracket(0)
b.load_team_stats()
print('Loaded')
b.save_team_stats()
print('Saved')
