import requests
from bs4 import BeautifulSoup
from myapp import models
from myapp.models import Player
import re


def get_name_id_dict(current_player_id):
    all_player_objs = Player.objects.all()
    player_name_id_dict = {}
    for player in all_player_objs:
        if player.player_id == current_player_id:
            pass
        else:
            if player.full_name == player.long_name or player.long_name == None:
                player_name_and_long_name = player.full_name
            else:
                player_name_and_long_name = str(player.full_name) + ' (' + str(player.long_name) + ')'
            player_name_id_dict[player_name_and_long_name] = str(player.player_id)
    return player_name_id_dict