from django import template
from myapp.models import Player
from myapp.content.constants import *

register = template.Library()


@register.filter
def position(all_players_list, position):
    players_list = Player.objects.filter(position_general=position)
    if position == "" : players_list = Player.objects.all()
    return players_list

@register.filter
def attributes(player, key_attr):
    if key_attr == "scorers":
        necessary_attrs = [getattr(player, attr) for attr in SCORERS_ATTRS]
    elif key_attr == "aggression":
        necessary_attrs = [getattr(player, attr) for attr in AGGRESSION_ATTRS]
    elif key_attr == "assistants":
        necessary_attrs = [getattr(player, attr) for attr in ASSISTANTS_ATTRS]
    elif key_attr == "sb_index":
        necessary_attrs = [getattr(player, attr) for attr in SB_INDEX_ATTRS]
    elif key_attr == "injury_prone":
        necessary_attrs = [getattr(player, attr) for attr in INJURY_PRONE_ATTRS]
    return necessary_attrs
