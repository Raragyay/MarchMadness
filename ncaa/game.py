from ncaa.team import Team


class Game:
    def __init__(self):
        self.team_1 = None
        self.team_2 = None

        self.team_references = {
            0: self.team_1,
            1: self.team_2
        }

    def scrape_load(self, soup, region_name):
        team_names = soup.find_all('li', class_='team')
        team_1_name = team_names[0].find('span', class_='name').text
        team_2_name = team_names[1].find('span', class_='name').text

        team_1_seed = int(team_names[0].find('span', class_='seed').text)
        team_2_seed = int(team_names[1].find('span', class_='seed').text)

        team_1_score = int(team_names[0].find('span', class_='score').text)
        team_2_score = int(team_names[1].find('span', class_='score').text)

        self.team_references[0] = self.team_1 = Team(
                {'name': team_1_name, 'seed': team_1_seed, 'region': region_name, 'score': team_1_score})
        # TODO: Make this more legible.
        self.team_references[1] = self.team_2 = Team(
                {'name': team_2_name, 'seed': team_2_seed, 'region': region_name, 'score': team_2_score})
        print(soup)

    def load(self, team_info):
        print(team_info)
        for team_num, team in enumerate(team_info):
            self.team_references[team_num] = Team(team)

    def save(self):
        teams = {}
        for team_num, team in self.team_references.items():
            print(team)
            teams[team_num] = team.save()
        return teams
