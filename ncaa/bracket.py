import pprint

from jsoninterchange import loader, dumper
from ncaa.region import Region
from ncaa.team import Team
from urlconnection import soupify


class Bracket:
    def __init__(self):
        self.region_0 = Region()
        self.region_1 = Region()
        self.region_2 = Region()
        self.region_3 = Region()
        self.region_4 = Region()
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
        for region_num, region in enumerate(soup.find_all('li', class_='round0', limit=5)):
            region_name = self.region_names[region_num]
            print(region_num)
            for team in region.find_all('li', class_='team'):
                if not team.text:
                    continue
                # print(team)
                team_name = team.find('span', class_='name').text
                team_seed = int(team.find('span', class_='seed').text)
                team_score = int(team.find('span', class_='score').text)
                print(team_name)
                self.region_dict[region_num].add_team(
                        Team(name=team_name,
                             region=region_name,
                             seed=team_seed,
                             score=team_score))


b = Bracket()
b.load_team_stats()
b.save_team_stats()
