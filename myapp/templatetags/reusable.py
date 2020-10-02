from django import template
from myapp.models import Player
from myapp.content.constants import *

register = template.Library()
@register.inclusion_tag('stats_table.html')
def stats_tables(player_attr, player_position):
    all_players_list = Player.objects.all()
    for player in all_players_list:
        if player.full_name == None: 
            all_players_list.exclude(player)
    stats_table_header = ""
    player_key_position = player_position
    player_key_attribute = player_attr
    if player_attr == "scorers":
        necessary_attrs_names = SCORERS_ATTRS_NAMES
        all_players_list = sorted(all_players_list, key=lambda x: x.goals_90, reverse=True)
        if player_position == '': stats_table_header = "Minutes per goal - best players"
        else: stats_table_header = "Goals/90 minutes - best %ss" % player_position.lower()
    elif player_attr == "aggression":
        necessary_attrs_names = AGGRESSION_ATTRS_NAMES
        all_players_list = sorted(all_players_list, key=lambda x: x.sb_aggression_index, reverse=True)
        if player_position == '': stats_table_header = "Most aggressive players"
        else: stats_table_header = "Most aggressive %ss" % player_position.lower()
    elif player_attr == "assistants":
        necessary_attrs_names = ASSISTANTS_ATTRS_NAMES
        all_players_list = sorted(all_players_list, key=lambda x: x.assists_90, reverse=True)
        if player_position == '': stats_table_header = "Minutes per assist - best players"
        else: stats_table_header = "Assists/90 minutes - best %ss" % player_position.lower()
    elif player_attr == "sb_index":
        necessary_attrs_names = SB_INDEX_ATTRS_NAMES
        all_players_list = sorted(all_players_list, key=lambda x: x.total_sb_index, reverse=True)
        if player_position == '': stats_table_header = "Best players"
        else: stats_table_header = "Best %ss" % player_position.lower()
    elif player_attr == "injury_prone":
        necessary_attrs_names = INJURY_PRONE_ATTRS_NAMES
        all_players_list = sorted(all_players_list, key=lambda x: x.total_games_injured, reverse=True)
        if player_position == '': stats_table_header = "Most injury-prone players"
        else: stats_table_header = "Most injury-prone %ss" % player_position.lower()

    
    return {'stats_table_header': stats_table_header, 'necessary_attrs_names': necessary_attrs_names, 'all_players_list': all_players_list, 'player_key_attribute': player_key_attribute, 'player_key_position': player_key_position}
