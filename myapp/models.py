from django.db import models
from myapp.content.constants import *
import requests
from bs4 import BeautifulSoup
import re
import json

class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'

class Player(models.Model):
    # B I O
    full_name = models.CharField(max_length=500, blank=True, null=True)
    long_name = models.CharField(max_length=500, blank=True, null=True)
    player_id = models.IntegerField()
    profile_img_url = models.URLField(max_length=1500, blank=True, null=True)
    nationality = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.CharField(max_length=500, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    position_general = models.CharField(max_length=50, blank=True, null=True)
    club = models.CharField(max_length=50, blank=True, null=True)
    club_img_url = models.URLField(max_length=1500, blank=True, null=True)
    national_team = models.CharField(max_length=50, blank=True, null=True)
    national_team_img_url = models.URLField(max_length=1500, blank=True, null=True)
    # S T A T S  -  G E N E R A L 
    played_seasons = models.IntegerField(blank=True, null=True)
    played_games_club = models.IntegerField(blank=True, null=True)
    played_games_national = models.IntegerField(blank=True, null=True)
    played_games = models.IntegerField(blank=True, null=True)
    total_games_injured = models.IntegerField(blank=True, null=True)
    total_days_injured = models.IntegerField(blank=True, null=True)
    goals_club = models.IntegerField(blank=True, null=True)
    goals_national = models.IntegerField(blank=True, null=True)
    goals = models.IntegerField(blank=True, null=True)
    assists_club = models.IntegerField(blank=True, null=True)
    assists_national = models.IntegerField(blank=True, null=True)
    assists = models.IntegerField(blank=True, null=True)
    minutes_club = models.IntegerField(blank=True, null=True)
    minutes_national = models.IntegerField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    cc = models.IntegerField(blank=True, null=True)
    goals_90 = models.FloatField(blank=True, null=True)
    assists_90 = models.FloatField(blank=True, null=True)
    cc_90 = models.FloatField(blank=True, null=True)
    yellow_cards = models.IntegerField(blank=True, null=True)
    red_cards = models.IntegerField(blank=True, null=True)
    total_cards_weighted = models.IntegerField(blank=True, null=True)
    yc90 = models.FloatField(blank=True, null=True)
    rc90 = models.FloatField(blank=True, null=True)
    sb_aggression_index = models.FloatField(blank=True, null=True)
    seasons_active = models.CharField(max_length=500, blank=True, null=True)
    goals_types_club = models.CharField(max_length=500, blank=True, null=True)
    goals_types_national = models.CharField(max_length=500, blank=True, null=True)
    goals_types = models.CharField(max_length=500, blank=True, null=True)
    leagues_dict = models.CharField(max_length=50000, blank=True, null=True)
    sb_index_by_league = models.CharField(max_length=50000, blank=True, null=True)
    total_sb_index = models.FloatField(blank=True, null=True)
    season_competition_stats = models.CharField(max_length=50000, blank=True, null=True)
    detailed_stats = models.CharField(max_length=50000, blank=True, null=True)

    # O T H E R
    views_count = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    num_updates = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.full_name)

    # M E T H O D S   C R E A T I N G   A T T R I B U T E S

    def get_full_name(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        if player_profile_tm_page_content.find('div' , {'class': 'dataName'}) != None:
            player_tm_name = "N O B O D Y" if player_profile_tm_page_content.find('div', {'class': 'dataName'}) == None else player_profile_tm_page_content.    find('div', {'class': 'dataName'}).find('h1').text
        return player_tm_name
    
    def get_long_name(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        if player_profile_tm_page_content.find('table', {'class': 'auflistung'}).find('th') != None:
            player_tm_long_name = player_profile_tm_page_content.find('table', {'class': 'auflistung'}).find('td').text if (player_profile_tm_page_content. find('table', {'class': 'auflistung'}).find('th').text == "Full name:" or player_profile_tm_page_content.find('table', {'class': 'auflistung'}). find('th').text == "Name in home country:") else self.get_full_name(self.player_id)
        return player_tm_long_name
    
    def get_profile_img_url(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        if player_profile_tm_page_content != None:
            player_img_big = player_profile_tm_page_content.find('div', {'class': 'dataBild'}).find('img')['src']  
        else:
            "Not found"
        if "default" in player_img_big: player_img_big = "static/img/no_img.png"
        return player_img_big
    
    def get_nationality(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        player_tm_info_table_rows = player_profile_tm_page_content.find('table', {'class': 'auflistung'}).find_all('tr')
        for row in player_tm_info_table_rows: #there's no specific class for the tr elements, so I need to target it some other way
            if row.find('th').find(string=re.compile("Citizenship:")):
                player_tm_nationality = row.find('img')['title']
            else:
                "Unknown"
        return player_tm_nationality.replace("\'", "")
    
    def get_date_of_birth(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        player_tm_info_table_rows = player_profile_tm_page_content.find('table', {'class': 'auflistung'}).find_all('tr')
        for row in player_tm_info_table_rows:
            if row.find('th').find(string=re.compile("Date of birth:")):
                player_tm_date_of_birth = row.find('a').text
        return player_tm_date_of_birth
    
    def get_position(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        player_tm_info_table_rows = player_profile_tm_page_content.find('table', {'class': 'auflistung'}).find_all('tr')
        for row in player_tm_info_table_rows:
            if row.find('th').find(string=re.compile("Position:")):
                player_tm_position = row.find('td').text
        player_tm_position = player_tm_position.replace("  ", " ").replace("\n", "")
        return player_tm_position

    def get_position_general(self, player_id):
        position_lowercase = self.position.lower()
        if "goalkeeper" in position_lowercase : pos_general = "Goalkeeper"
        elif "back" in position_lowercase or "sweeper" in position_lowercase : pos_general = "Defense"
        elif "midfield" in position_lowercase : pos_general = "Midfield"
        elif "winger" in position_lowercase or "forward" in position_lowercase or "striker" in position_lowercase : pos_general = "Forward"
        else: pos_general = "Other"
        return pos_general


    def get_club(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        player_tm_info_table_rows = player_profile_tm_page_content.find('table', {'class': 'auflistung'}).find_all('tr')
        for row in player_tm_info_table_rows:
            if row.find('th').find(string=re.compile("Current club:")):
                player_tm_club = row.find_all('a')
        return player_tm_club[1].text

    def get_club_img_url(self, player_id):
        player_profile_tm_page_content = self.get_profilepage_content()
        club_img_url = player_profile_tm_page_content.find('div', {'class': 'dataZusatzImage'}).find('a').find('img')['src']
        return club_img_url

    def get_national_team(self, player_id):
        content = self.get_detailedstats_content()
        player_verification = content.find('p', {'class': 'notTablet'})
        if player_verification == None: # means that player has no national experience
            return "None"
        else:    
            national_team_name = player_verification.find('a', {'class': 'vereinprofil_tooltip'}).text
        return national_team_name

    def get_national_team_img_url(self, player_id):
        content = self.get_detailedstats_content()
        if not self.national_team == "None":
            nat_link = 'https://www.transfermarkt.co.uk' + content.find('p', {'class': 'notTablet'}).find('span', {'class': 'dataValue'}).find('a')['href']
            nat_content = get_gameinfo_page_content(nat_link)
            nat_img = nat_content.find('div', {'class': 'dataBild nationalmannschaft'}).find('img')['src']
        else:
            nat_img = ""
        return nat_img
    
    def get_played_seasons(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_body_row = content.find('table', {'class': 'items'}).find('tbody').find_all('tr')
        seasons_list = []
        regex = re.compile('zentriert')
        for row in stats_table_body_row:
            season = row.find('td', {'class': regex}).text
            if season in seasons_list:
                continue
            else:
                seasons_list.append(season)
        return len(seasons_list)

    def get_played_games_club(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_footer_cells = content.find('table', {'class': 'items'}).find('tfoot').find_all('td')
        return int(stats_table_footer_cells[4].text)

    def get_played_games_national(self, player_id):
        content = self.get_nationalstats_content()
        tr_list = []
        table_div = content.find('div', {'class': 'large-8'})
        if table_div == None: # means that player has no national experience
            return 0
        else: 
            all_table_rows = table_div.find('div', {'class': 'box'}).find('tbody').find_all('tr')
            for nat_team_row in all_table_rows:
                if nat_team_row not in tr_list: tr_list.append(nat_team_row) 
                if nat_team_row.find(string=re.compile("U1")) or nat_team_row.find(string=re.compile("U2")) or nat_team_row.find(string=re.compile("Olympic")): tr_list.remove(nat_team_row) # to get rid of junior national teams
                if len(tr_list) == 0:
                    played_games_national = 0
                else:
                    played_games_national = content.select('div.large-8.columns > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(5) > a')[0].text
        return int(played_games_national)

    def get_played_games(self, player_id):
        return self.played_games_club + self.played_games_national

    def get_total_games_injured(self, player_id):
        content = self.get_injuries_content()
        if content.find('div', {'id': 'yw1'}).find('table'):
            all_rows = content.find('div', {'id': 'yw1'}).find('table').find('tbody').find_all('tr')
            all_games = []
            for row in all_rows:
                last_cell = row.find_all('td')[-1].text
                all_games.append(int(last_cell)) if "-" not in last_cell else all_games.append(0)
            total_injured_games = sum(all_games)
        else: 
            total_injured_games = 0
        return total_injured_games

    def get_total_days_injured(self, player_id):
        content = self.get_injuries_content()
        if content.find('div', {'id': 'yw1'}).find('table'):
            all_rows = content.find('div', {'id': 'yw1'}).find('table').find('tbody').find_all('tr')
            all_days = []
            for row in all_rows:
                last_cell = row.find_all('td')[-2].text
                last_cell = re.sub('[^0-9]', '', last_cell)
                all_days.append(int(last_cell)) if "-" not in last_cell else all_days.append(0)
                all_days.append(int(last_cell))
            total_injured_days = sum(all_days)
        else: 
            total_injured_days = 0
        return total_injured_days
        
    def get_goals_club(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_footer_cells = content.find('table', {'class': 'items'}).find('tfoot').find_all('td')
        return int(stats_table_footer_cells[6].text)

    def get_goals_national(self, player_id):
        content = self.get_nationalstats_content()
        tr_list = []
        table_div = content.find('div', {'class': 'large-8'})
        if table_div == None: # means that player has no national experience
            return 0
        else: 
            all_table_rows = table_div.find('div', {'class': 'box'}).find('tbody').find_all('tr')
            for nat_team_row in all_table_rows:
                if nat_team_row not in tr_list: tr_list.append(nat_team_row) 
                if nat_team_row.find(string=re.compile("U1")) or nat_team_row.find(string=re.compile("U2")) or nat_team_row.find(string=re.compile("Olympic")): 
                    tr_list.remove(nat_team_row) # to get rid of junior national teams
                if len(tr_list) == 0:
                    national_goals = 0
                else:
                    national_goals = content.select('div.large-8.columns > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(6) > a')[0].text
        return int(national_goals)

    def get_goals(self, player_id):
        return self.goals_club + self.goals_national


    def get_assists_club(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_footer_cells = content.find('table', {'class': 'items'}).find('tfoot').find_all('td')
        return int(stats_table_footer_cells[7].text)

    def get_assists_national(self, player_id):
        content = self.get_nationalstats_content()
        assists = int(content.find('div', {'class': 'responsive-table'}).find('table').find('tfoot').find('tr').find_all('td')[4].text if content.find('div', {'class': 'responsive-table'}).find('table').find('tfoot').find('tr').find_all('td')[4].text != "-" else 0)
        return assists

    def get_assists(self, player_id):
        return self.assists_club + self.assists_national


    def get_minutes_club(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_footer_cells = content.find('table', {'class': 'items'}).find('tfoot').find_all('td')
        if "." in stats_table_footer_cells[9].text: 
            played_minutes = stats_table_footer_cells[9].text.replace(".", "")
            played_minutes2 = played_minutes.replace("'", "")
        return int(played_minutes2)

    def get_minutes_national(self, player_id):
        content = self.get_nationalstats_content()
        player_verification = content.find('form', {'class': 'js-form-params2path'})
        if player_verification == None: # means that player has no international experience
            return 0
        else:
            national_team_name = content.find('form', {'class': 'js-form-params2path'}).find('div', {'class': 'inline-select'}).find('option').text
            if national_team_name.count("U1") > 0 or national_team_name.count("U2") > 0 or national_team_name.count("Olympic") > 0: #means that player has only junior international experience
                return 0
            else: 
                national_apps_mins = content.find('div', {'id': 'yw1'}).find('table', {'class': 'items'}).find('tfoot').find_all('td')[-1].text
                nat_mins = convert_tm_mins_to_int(national_apps_mins)
        return int(nat_mins)

    def get_minutes(self, player_id):
        return self.minutes_club + self.minutes_national
    
    def get_cc(self, player_id):
        return self.goals + self.assists
    
    def get_goals_90(self, player_id):
        goals_90 = round(self.goals/(self.minutes/90), 2)
        return goals_90
    
    def get_assists_90(self, player_id):
        assists_90 = round(self.assists/(self.minutes/90), 2)
        return assists_90
    
    def get_cc_90(self, player_id):
        cc_90 = round(self.cc/(self.minutes/90), 2)
        return cc_90



    def get_yellow_cards(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_footer_cells = content.find('table', {'class': 'items'}).find('tfoot').find_all('td')
        yellow_cards = stats_table_footer_cells[8].text.partition("/")[0]
        if "-" in yellow_cards: yellow_cards = yellow_cards.replace("-", "0")
        second_yellow_cards = stats_table_footer_cells[8].text.partition("/")[2].partition("/")[0].replace(" ", "")
        if "-" in second_yellow_cards: second_yellow_cards = second_yellow_cards.replace("-", "0")
        return int(yellow_cards) + int(second_yellow_cards)

    def get_red_cards(self, player_id):
        content = self.get_detailedstats_content()
        stats_table_footer_cells = content.find('table', {'class': 'items'}).find('tfoot').find_all('td')
        red_cards = stats_table_footer_cells[8].text.partition("/")[2].partition("/")[2]
        if "-" in red_cards: red_cards = red_cards.replace("-", "0")
        return int(red_cards)

    def get_total_cards_weighted(self, player_id):
        return self.yellow_cards + self.red_cards*3

    def get_yc90(self, player_id):
        yc90 = round(self.yellow_cards/(self.minutes/90), 2)
        return yc90

    def get_rc90(self, player_id):
        if self.red_cards != 0: rc90 = round(self.red_cards/(self.minutes/90), 2)
        else: rc90 = 0
        return rc90

    def get_sb_aggression_index(self, player_id):
        return float(round((self.total_cards_weighted / self.minutes )*10000, 2))

    def get_seasons_active(self, player_id):
        content = self.get_detailedstats_content()
        all_seasons_options = content.find('select', {'name': 'saison'}).find_all('option')
        seasons_list = []
        for i in range (len(all_seasons_options)):
            if all_seasons_options[i]['value'] != '':
                seasons_list.append(int(all_seasons_options[i]['value']))
        return list(reversed(seasons_list))

    def get_goals_types_club(self, player_id):
        allgoals_content = self.get_allgoals_content()
        table_rows = allgoals_content.select('#main > div:nth-child(17) > div.large-8.columns > div > div.responsive-table > table > tbody')[0].find_all('tr')
        allgoals_list = []
        for row in table_rows:
            if len(row) == 3: # it helps to recognize if a table row is a separator or not
                pass
            else:
                goal_type = row.find_all('td')[-1].text
                if goal_type == "": goal_type = "Unknown"
                allgoals_list.append(goal_type)
        get_ordered_goal_types_dict(allgoals_list)
        return get_ordered_goal_types_dict(allgoals_list)

    def get_goals_types_national(self, player_id):
        national_content = self.get_nationalstats_content()
        national_goals_num = int(national_content.find('table').find('tbody').find_all('tr')[1].find_all('td')[5].text.replace("-", "0")) if "U1" not in national_content.find('table').find('tbody').find_all('tr')[1].find_all('td')[1].text and "U2" not in national_content.find('table').find('tbody').find_all('tr')[1].find_all('td')[1].text and "Olympic" not in national_content.find('table').find('tbody').find_all('tr')[1].find_all('td')[1].text else 0
        try:# sometimes transfermarkt has issues with showing up national statistics, I need to work around this somehow
            table_rows = national_content.find_all('div', {'class': 'responsive-table'})[1].find('table').find('tbody').find_all('tr')
        except IndexError:
            table_rows = None
        if table_rows != None:
            games_with_goals_urls = []
            for row in table_rows:
                if len(row) > 22:
                    try:
                        goal_num = 0 if row.find_all('td')[-6].text == "" else int(row.find_all('td')[-6].text)
                        if goal_num > 0:
                            game_with_goal_url = "https://www.transfermarkt.co.uk" + row.find_all('td')[-8].find('a')['href']
                            games_with_goals_urls.append(game_with_goal_url)
                    except IndexError:
                        continue
            allgoals_list = []
            important_cells = []
            for game_url in games_with_goals_urls: 
                gamepage_content = get_gameinfo_page_content(game_url)
                goalscorers_table = gamepage_content.find('div' , {'id': 'sb-tore'}) if gamepage_content.find('div' , {'id': 'sb-tore'}) else "None"
                goalscorers_row = goalscorers_table.find_all('li')
                goalscorers_cells = []
                for row in goalscorers_row:
                    goalscorers_cell = row.find('div' , {'class': 'sb-aktion-aktion'})
                    #if "Assist" in goalscorers_cell: goalscorers_cell = goalscorers_cell.split("Assist", 1)[0]
                    goalscorers_cells.append(goalscorers_cell) 
                for cell in goalscorers_cells:
                    if cell.find('a')['title'] == self.full_name:
                        if "Assist" in cell.text: 
                            cell_text = cell.text.split("Assist", 1)[0] 
                        else:
                            cell_text = cell.text
                        important_cells.append(cell_text)
            for cell in important_cells: 
                allgoals_list.append(verify_goal_type(cell))
        else: 
            allgoals_list = ["Unknown"] * national_goals_num
        return get_ordered_goal_types_dict(allgoals_list)

    def get_goals_types(self, player_id):
        goals_types_club = self.get_goals_types_club(self.player_id)
        goals_types_national = self.get_goals_types_national(self.player_id)
        summed_dict = {}
        for key in goals_types_club.keys():
            summed_dict[key] = int(goals_types_club[key]) + int(goals_types_national[key])
        return summed_dict

    def get_leagues_dict(self, player_id):
        player_page_content = self.get_detailedstats_content()
        player_leagues_rows = player_page_content.find('div', {'id': 'yw1'}).find('table').find('tbody').find_all('tr')
        for row in player_leagues_rows:
            if len(row) < 6: player_leagues_rows.remove(row)
        comp_ids = []
        for row in player_leagues_rows:
            comp_id = row.find_all('td')[2].find('a')['href'].partition('saison_id')[0].split("/")[-2]
            if comp_id not in comp_ids: comp_ids.append(comp_id)
        player_league_dict = {}
        player_national_dict = {}
        for c_id in comp_ids:
            comppage_content = self.get_compstats_content(c_id)
            comp_row = comppage_content.find('div', {'id': 'yw1'}).find('table').find('tbody').find('tr')
            comp_link = 'https://www.transfermarkt.co.uk' + comp_row.find_all('td')[2].find('a')['href']
            leaguepage_content = get_gameinfo_page_content(comp_link)
            if leaguepage_content.find('div', {'id': 'wettbewerb_head'}).find('div', {'class': 'box-header'}):
                comp_name = leaguepage_content.find('div', {'id': 'wettbewerb_head'}).find('div', {'class': 'box-header'}).find('h1').text.replace("'", "")
            else:
                comp_name = leaguepage_content.find('div', {'id': 'wettbewerb_head'}).find('h1', {'itemprop': 'name'}).text.replace("'", "")
            comp_games = int(comppage_content.find('div', {'id': 'yw1'}).find('table').find('tfoot').find_all('td')[4].text.replace("-", "0"))
            comp_goals = int(comppage_content.find('div', {'id': 'yw1'}).find('table').find('tfoot').find_all('td')[6].text.replace("-", "0"))
            comp_assists = int(comppage_content.find('div', {'id': 'yw1'}).find('table').find('tfoot').find_all('td')[7].text.replace("-", "0"))
            comp_minutes = int(comppage_content.find('div', {'id': 'yw1'}).find('table').find('tfoot').find_all('td')[9].text.replace("-", "0").replace("'", "").replace(".", ""))
            comp_sb_index = calculate_sb_index(comp_goals, comp_assists, comp_minutes, get_league_weight(comp_name))
            player_league_dict[comp_name] = {'name': comp_name, 'games': comp_games, 'goals': comp_goals, 'assists': comp_assists, 'minutes': comp_minutes, 'weight': get_league_weight(comp_name), 'sb_index': comp_sb_index}
            player_national_dict['National Team'] = {'name': self.national_team, 'games': self.played_games_national, 'goals': self.goals_national, 'assists': self.assists_national, 'minutes': self.minutes_national, 'weight': get_league_weight('National Team'), 'sb_index': calculate_sb_index(self.goals_national, self.assists_national, self.minutes_national, get_league_weight('National Team'))}
            player_league_dict.update(player_national_dict)
        return player_league_dict

    def get_sb_index_by_league(self, player_id):
        '''all_player_leagues = [x for x in self.get_leagues_dict(self.player_id).keys() if x != 'name' and x != 'games' and x != 'goals' and x != 'assists' and x != 'minutes' and x != 'weight']
        league_sb_index_dict = {}
        leagues_dict = json.loads(self.leagues_dict.replace("'", "\""))
        for league in all_player_leagues:
            minutes = leagues_dict[league]['minutes']
            goals = leagues_dict[league]['goals']
            assists = leagues_dict[league]['assists']
            weight = leagues_dict[league]['weight']
            try:
                league_sb_index = calculate_sb_index(goals, assists, minutes, weight)
            except ZeroDivisionError:
                league_sb_index = 0
            league_sb_index_dict[league] = league_sb_index'''
        sb_index_by_league_dict = {}
        all_player_leagues = self.get_leagues_dict(self.player_id).keys()
        for league in all_player_leagues:
            sb_index_by_league_dict[league] = self.get_leagues_dict(self.player_id)[league]["sb_index"]
        return sb_index_by_league_dict

    def get_total_sb_index(self, player_id):
        return round(sum([x for x in self.get_sb_index_by_league(self.player_id).values()]), 2)

    def get_season_competition_stats(self, player_id):
        all_season_comps_stats = {}
        total_season_sb_index_list = []
        for season in json.loads(self.seasons_active.replace("'", "\"")):
            content = self.get_seasonalstats_content(season)
            season_comps = []
            season_comps_stats = {}
            comp_stats = {}
            comp_sb_index = []
            if content.find('div', {'id': 'yw1'}).find('table'):
                competition_rows = content.find('div', {'id': 'yw1'}).find('table').find('tbody').find_all('tr')
                for row in competition_rows:
                    comp_link = 'https://www.transfermarkt.co.uk' + row.find_all('td')[1].find('a')['href']
                    comppage_content = get_gameinfo_page_content(comp_link)
                    if comppage_content.find('div', {'id': 'wettbewerb_head'}).find('div', {'class': 'box-header'}):
                        comp_name = comppage_content.find('div', {'id': 'wettbewerb_head'}).find('div', {'class': 'box-header'}).find('h1').text.replace("'", "")
                    else:
                        comp_name = comppage_content.find('div', {'id': 'wettbewerb_head'}).find('h1', {'itemprop': 'name'}).text.replace("'", "")
                    comp_goals = int(row.find_all('td')[5].text) if row.find_all('td')[5].text != "-" else 0
                    comp_assists = int(row.find_all('td')[6].text) if row.find_all('td')[6].text != "-" else 0
                    comp_minutes = int(row.find_all('td')[8].text.replace(".", "").replace("'", "")) if row.find_all('td')[8].text != "-" else 0
                    comp_stats[comp_name] = {'name': comp_name, 'goals': comp_goals, 'assists': comp_assists, 'minutes': comp_minutes, 'comp_sb_index':     calculate_sb_index(comp_goals, comp_assists, comp_minutes, get_league_weight(comp_name))} 
                    comp_sb_index.append(comp_stats[comp_name]['comp_sb_index'])
            else:
                comp_stats["None"] = {'name': "None", 'goals': 0, 'assists': 0, 'minutes': 0, 'comp_sb_index': 0} # we need to add this, otherwise there will be some problems with charts in players profile - seasons will be calculated incorrectly
                comp_sb_index.append(comp_stats["None"]['comp_sb_index'])
            season_comps_stats[str(season)] = comp_stats
            total_season_sb_index_list.append(comp_sb_index)
            all_season_comps_stats.update(season_comps_stats)
        total_season_sb_index = []
        sb_index_by_season = {}
        for season in total_season_sb_index_list:
            total_season_sb_index.append(round(sum([x for x in season]), 2))
        sb_index_by_season['sb_index_by_season'] = total_season_sb_index
        all_season_comps_stats.update(sb_index_by_season)
        return all_season_comps_stats

    def get_detailed_stats(self, player_id):
        seasons_active = self.get_seasons_active(self.player_id)
        season_games_list = self.get_stat_by_season('#yw1 > table > tfoot > tr > td:nth-child(4)')
        season_minutes_list = self.get_stat_by_season('#yw1 > table > tfoot > tr > td:nth-child(9)')
        season_goals_list = self.get_stat_by_season('#yw1 > table > tfoot > tr > td:nth-child(6)')
        season_assists_list = self.get_stat_by_season('#yw1 > table > tfoot > tr > td:nth-child(7)')
        season_cc_list = []
        '''season_sb_index_list = []
        for season_idx in seasons_active:'''
        for season_idx in range(len(season_minutes_list)):
            cc = season_goals_list[season_idx] + season_assists_list[season_idx]
            season_cc_list.append(cc)
        season_total_cards_list_raw = self.get_stat_by_season('#yw1 > table > tfoot > tr > td:nth-child(8)')
        season_total_cards_list = []
        for season in season_total_cards_list_raw:
            season_data = season.replace('\xa0', '')
            season_total_cards_list.append(season_data)
        season_yc_list = []
        for season in season_total_cards_list:
            yc = season.partition("/")[0]
            if "-" in yc: yc = yc.replace("-", "0")
            second_yc = season.partition("/")[2].partition("/")[0].replace(" ", "").replace("-", "0")
            if second_yc == "": second_yc = "0"
            yc_and_second_yc = int(yc) + int(second_yc)
            season_yc_list.append(yc_and_second_yc)
            season_rc_list = []
        for season in season_total_cards_list:
            rc = season.partition("/")[2].partition("/")[2].replace("-", "0")
            if rc == "": rc = "0"
            season_rc_list.append(int(rc))
        season_club_img_list = []
        for season in seasons_active:
            content = self.get_seasonalstats_content(season)
            if content.select('#yw1 > table'):
                season_club_img = content.select('#yw1 > table > tbody > tr:nth-child(1) > td.hauptlink.no-border-rechts.zentriert')[0].find('a').find  ('img')['src']
                season_club_img_list.append(season_club_img)
            else:
                season_club_img = ''
                season_club_img_list.append(season_club_img)
        season_g90_list = []
        season_a90_list = []
        season_cc90_list = []
        for season_idx in range(len(season_minutes_list)):
            season_g90 = round(season_goals_list[season_idx]/(season_minutes_list[season_idx]/90), 2) if season_goals_list[season_idx] != 0 and season_minutes_list[season_idx] != 0 else 0
            season_a90 = round(season_assists_list[season_idx]/(season_minutes_list[season_idx]/90), 2) if season_assists_list[season_idx] != 0 and season_minutes_list[season_idx] != 0 else 0
            season_cc90 = round(season_cc_list[season_idx]/(season_minutes_list[season_idx]/90), 2)  if season_cc_list[season_idx] != 0 and season_minutes_list[season_idx] != 0 else 0
            season_g90_list.append(season_g90)
            season_a90_list.append(season_a90)
            season_cc90_list.append(season_cc90)

        detailed_stats_dict = {
            'name': self.full_name,
            'long_name': self.long_name,
            'id': self.player_id,
            'date_of_birth': self.date_of_birth,
            'position': self.position,
            'club': self.club,
            'seasons': seasons_active,
            'games': season_games_list, 
            'total_games_injured': self.total_games_injured,
            'minutes': season_minutes_list,
            'goals': season_goals_list,
            'assists': season_assists_list,
            'yellow_cards': season_yc_list,
            'red_cards': season_rc_list,
            'club_img': season_club_img_list,
            'cc': season_cc_list,
            'g90': season_g90_list,
            'a90': season_a90_list,
            'cc90': season_cc90_list,
            'goals_types_club': self.goals_types_club,
            'goals_types_national': self.goals_types_national,
            'goals_types': self.goals_types,
            'leagues_dict': self.leagues_dict,
            'sb_index_by_league': self.sb_index_by_league,
            'total_sb_index': self.total_sb_index,
            }
        return detailed_stats_dict

# U S E F U L   M E T H O D S

    def get_detailedstats_content(self):
        player_tm_detailedstats_url_id = "https://www.transfermarkt.co.uk/lionel-messi/leistungsdatendetails/spieler/{}".format(self.player_id)
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(player_tm_detailedstats_url_id, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_seasonalstats_content(self, season):
        player_tm_seasonalstats_url_id = "https://www.transfermarkt.co.uk/lionel-messi/leistungsdatendetails/spieler/{}/plus/0?saison={}&verein=&liga=&wettbewerb=&pos=&trainer_id=".format(self.player_id, season)
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(player_tm_seasonalstats_url_id, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_profilepage_content(self):
        player_tm_profilepage_url_id = "https://www.transfermarkt.co.uk/silvio-adzic/profil/spieler/{}".format(self.player_id)
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(player_tm_profilepage_url_id, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_nationalstats_content(self):
        player_tm_nationalstats_url_id = "https://www.transfermarkt.co.uk/mario-basler/nationalmannschaft/spieler/{}".format(self.player_id)
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(player_tm_nationalstats_url_id, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_allgoals_content(self):
        player_tm_allgoals_url_id = "https://www.transfermarkt.co.uk/ronaldo/alletore/spieler/{}".format(self.player_id)
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(player_tm_allgoals_url_id, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_injuries_content(self):
        player_tm_injuries_url_id = "https://www.transfermarkt.co.uk/andriy-shevchenko/verletzungen/spieler/{}".format(self.player_id)
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(player_tm_injuries_url_id, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_compstats_content(self, comp_id):
        base_url = f"https://www.transfermarkt.co.uk/andriy-shevchenko/leistungsdatendetails/spieler/{self.player_id}/plus/0?saison=&verein=&liga=&wettbewerb={comp_id}&pos=&trainer_id="
        headers = {'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        return soup

    def get_all_attributes(self):
        tuple_of_fields = self._meta.get_fields()
        sanitized_list = []
        for field in tuple_of_fields:
            sanitized_field = str(field).replace("myapp.Player.", "")
            sanitized_list.append(sanitized_field)
        if "id" and "created" and "num_updates" and "player_id" in sanitized_list: 
            sanitized_list.remove("id")
            sanitized_list.remove("created")
            sanitized_list.remove("num_updates")
            sanitized_list.remove("player_id")
        return sanitized_list

    def get_all_methods(self):
        object_all_properties = dir(self) # dir returns list sorted aphabetically, I need different order of a list, that's why last 5 lines of this function looks this way
        object_methods_sorted_improperly = []
        for element in object_all_properties:
            if element.startswith("get"):
                object_methods_sorted_improperly.append(element)
        unnecessary_methods = ["get_deferred_fields", "get_detailedstats_content", "get_next_by_created", "get_previous_by_created",    "get_profilepage_content"]
        for method in unnecessary_methods:
            if method in object_methods_sorted_improperly:
                object_methods_sorted_improperly.remove(method)
        attrs_list = self.get_all_attributes()
        object_methods_sorted_properly = []
        for attr in attrs_list:
            for obj_method in object_methods_sorted_improperly:
                if "get_" + attr == obj_method:
                    object_methods_sorted_properly.append(obj_method)
        return object_methods_sorted_properly

    def get_all_values(self):
        object_all_attributes = self.get_all_attributes()
        object_all_values = []
        for attr in object_all_attributes: 
            field_object = self._meta.get_field(attr)
            value = field_object.value_from_object(self)
            object_all_values.append(value)
        return object_all_values

    def get_attrs_values_dict(self):
        object_dict = {}
        object_all_attributes = self.get_all_attributes()
        object_all_values = []
        for attr in object_all_attributes: 
            field_object = self._meta.get_field(attr)
            value = field_object.value_from_object(self)
            object_all_values.append(value)
        for idx, item in enumerate(object_all_attributes):
            object_dict[item] = object_all_values[idx]
        return object_dict

# H E L P E R S
    def get_stat_by_season(self, selector):
        season_stat_list = []
        for season in self.get_seasons_active(self.player_id):
            content = self.get_seasonalstats_content(season)
            if content.select('#yw1 > table'):
                season_stat = content.select(selector)[0].text
                if season_stat == '-': season_stat = '0'
            else:
                season_stat = '0'
            if "'" in season_stat: season_stat = season_stat.replace("'", "")
            if "." in season_stat: season_stat = season_stat.replace(".", "")
            if selector != '#yw1 > table > tfoot > tr > td:nth-child(8)': season_stat = int(season_stat)
            season_stat_list.append(season_stat)
            
        return season_stat_list
        
def convert_tm_mins_to_int(string):
    if "'" in string: new_string = string.replace("'", "")
    if "." in string: new_string = new_string.replace(".", "")
    return int(new_string)

def unify_seasons_digits_list(seasons_list):
    correct_seasons_list = []
    for season in seasons_list:
        if len(season) == 5: # means that in this case we've got two digits seasons names separated by /, e.g. 07/08
            new_season_str_two_digits = season.replace(season[2:len(season)], '')
            if int(new_season_str_two_digits) < 30: 
                new_season = list(new_season_str_two_digits)
                new_season.insert(0, '20')
                new_season = int(''.join(new_season))
                correct_seasons_list.append(new_season)
            else:
                new_season = list(new_season_str_two_digits)
                new_season.insert(0, '19')
                new_season = int(''.join(new_season))
                correct_seasons_list.append(new_season)
        elif len(season) == 4: # for leagues where one season = one year, e.g. Brazil: 2001
            correct_seasons_list.append(int(season))
    return correct_seasons_list

def get_gameinfo_page_content(url):
    headers = {'User-Agent': 
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    pageTree = requests.get(url, headers=headers)
    soup = BeautifulSoup(pageTree.content, 'html.parser')
    return soup


def get_ordered_goal_types_dict(allgoals_list):
    right_footed_shot = allgoals_list.count('Right-footed shot')
    left_footed_shot = allgoals_list.count('Left-footed shot')
    header = allgoals_list.count('Header')
    penalty = allgoals_list.count('Penalty')
    direct_free_kick = allgoals_list.count('Direct free kick')
    long_distance_kick = allgoals_list.count('Long distance kick')
    tap_in = allgoals_list.count('Tap-in') + allgoals_list.count('Penalty rebound')
    other = allgoals_list.count('Counter attack goal') + allgoals_list.count('Solo run') + allgoals_list.count('Deflected shot on goal') + allgoals_list.count('Chest') + allgoals_list.count('Direct corner')
    unknown = allgoals_list.count('Unknown')
    goal_type_dict = {
        'right_footed_shot': right_footed_shot,
        'left_footed_shot': left_footed_shot,
        'header': header,
        'penalty': penalty,
        'direct_free_kick': direct_free_kick,
        'long_distance_kick': long_distance_kick,
        'tap_in': tap_in,
        'other': other,
        'unknown': unknown,
    }
    return goal_type_dict

def verify_goal_type(string):
    all_possible_goal_types = ['Right-footed shot', 'Left-footed shot', 'Header', 'Penalty', 'Direct free kick', 'Long distance kick', 'Penalty rebound', 'Counter attack goal', 'Solo run', 'Deflected shot on goal', 'Chest', 'Direct corner', 'Unknown']
    for goal_type in all_possible_goal_types:
        if goal_type in string:
            type_of_goal = goal_type
            break
        else: 
            type_of_goal = "Unknown"
            continue
    return type_of_goal 

def get_league_weight(league_name):
    if league_name in leagues_weights.keys(): #leagues_weights can be found in constants file
        league_weight = leagues_weights[league_name]
    else: league_weight = 0
    return league_weight

def calculate_sb_index(goals, assists, minutes, weight):
    try:
        return round((((goals + assists) / (minutes/90)) * weight) * (minutes / 1000), 2)
    except ZeroDivisionError: 
        return 0


####################

class League(models.Model):
    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(max_length=500, blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    
def get_leagues_weights():
    for league in League.objects.all():
        league.weight = leagues_weights[league.name]
        league.save()
###