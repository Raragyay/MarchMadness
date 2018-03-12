from urlconnection import soupify
# import pprint
import pandas as pd


def get_round_0_seeds(soup):
    """
    A small function that gets the seeds and opponents in the first round.
    :param soup: A soupified version of the url.
    :return: A DataFrame with three columns: Team Name, Seed, and First Round Opponent
    """
    team_seeds = []
    for region in soup.find_all('li', class_='round0', limit=5):
        for game in region.find_all('li', class_='game'):
            team_names = game.find_all('li', class_='team')
            team_1_name = team_names[0].find('span', class_='name').text
            team_2_name = team_names[1].find('span', class_='name').text
            team_1_seed = int(team_names[0].find('span', class_='seed').text)
            team_2_seed = int(team_names[1].find('span', class_='seed').text)
            if '/' not in team_1_name:
                team_seeds.append({'Team Name': team_1_name, 'Seed': team_1_seed, 'First Round Opponent': team_2_name})
            if '/' not in team_2_name:
                team_seeds.append({'Team Name': team_2_name, 'Seed': team_2_seed, 'First Round Opponent': team_1_name})
    df = pd.DataFrame(team_seeds, columns=['Team Name', 'Seed', 'First Round Opponent'])
    df.sort_values(['Seed'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    return df


round_0_seeds = get_round_0_seeds(
        soupify('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men'))
print(round_0_seeds)
