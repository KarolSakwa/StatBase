import requests
from django.shortcuts import render
from . import models
from myapp.content.helpers import *
from myapp.content.constants import *
from bs4 import BeautifulSoup
from myapp.models import Player, League, get_gameinfo_page_content, get_leagues_weights
from django.db.models import F, Q, Max
from django.core.serializers import serialize 

import json
import re


def home(request):
    all_players_list = Player.objects.all()
    most_popular = Player.objects.annotate(Max('views_count')).order_by('-views_count')[0:4]
    top_players = Player.objects.annotate(Max('total_sb_index')).order_by('-total_sb_index')[0:3]
    context = {
        'most_popular': most_popular,
        'top_players': top_players
    }
    return render(request, 'home.html', context)


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    queryset_list = Player.objects.filter(full_name__icontains=search)
    return render(request, 'myapp/new_search.html', {'queryset_list': queryset_list, 'search': search})


def player_profile(request, player_tm_id):
    sb_player = Player.objects.get(player_id=player_tm_id)
    Player.objects.filter(player_id=sb_player.player_id).update(views_count=F('views_count') + 1)
    sb_player.views_count += 1
    sent_names_id_dict = get_name_id_dict(sb_player.player_id) # this is a dictionary with names and IDs of players just for autocomplete function
    player_obj_js = sb_player.get_attrs_values_dict()
    context = {
        'sb_player': sb_player,
        'sent_names_id_dict': sent_names_id_dict,
        'player_obj_js': player_obj_js,
    }
    return render(request, 'myapp/player_profile.html', context)


def db_update(request):
    current_player_id = 7349 # 3187
    transferred_data = ""
    transferred_attr = ""
    next_attribute_index = 0
    
    if not Player.objects.filter(player_id=current_player_id).exists():
        models.Player.objects.create(
            player_id=current_player_id)
    sb_player = Player.objects.get(player_id=current_player_id)
    methods_list = sb_player.get_all_methods()
    attributes_list = sb_player.get_all_attributes()
    attribute_count = []
    for i in range (10000):
        if len(attribute_count) == 0:
            sb_player = Player.objects.get(player_id=current_player_id)
            current_player_id += 1
            attribute_count = [attribute for attribute in attributes_list if getattr(sb_player, attribute) == None]
            for idx, attribute in enumerate(attributes_list):
                if getattr(sb_player, attribute) == None:
                    next_attribute = attribute
                    next_attribute_index = idx
                    break

    if request.POST.get('get_new_button'):
        value = getattr(sb_player, methods_list[next_attribute_index])()
        setattr(sb_player, next_attribute, value)
        transferred_data = value
        transferred_attr = attributes_list[next_attribute_index]
        sb_player.save()

    all_db_players_num = len(Player.objects.all())
    context = {
        'sb_player': sb_player,
        'transferred_data': transferred_data,
        'transferred_attr': transferred_attr,
        'next_attribute_index': next_attribute_index,
        'next_attribute': next_attribute,
        'all_db_players_num': all_db_players_num,
        'attribute_count': attribute_count,
    }
    return render(request, 'myapp/db_update.html', context)

def db_updating_page(request):
    return render(request, 'myapp/db_updating_page.html')

def js_test(request):
    test_player = Player.objects.get(player_id=3332)
    test_var = ''


    context = {
        'test_var': test_var,
        'test_player': test_player,
    }

    return render(request, 'myapp/js_test.html', context)


def all_90_scorers(request):
    return render(request, 'myapp/all_90_scorers.html')


def gk_90_scorers(request):
    return render(request, 'myapp/gk_90_scorers.html')


def df_90_scorers(request):
    return render(request, 'myapp/df_90_scorers.html')


def mf_90_scorers(request):
    return render(request, 'myapp/mf_90_scorers.html')


def cf_90_scorers(request):
    return render(request, 'myapp/cf_90_scorers.html')

def injury_prone(request):
    return render(request, 'myapp/injury_prone.html')


def most_aggressive(request):
    return render(request, 'myapp/most_aggressive.html')


def most_assists(request):
    return render(request, 'myapp/most_assists.html')

def top_players(request):
    return render(request, 'myapp/top_players.html')


def top_scorers_chart(request):
    all_players = Player.objects.all()
    final_players_list = []
    for player in all_players: 
        if player.goals_90 != None: final_players_list.append(player)
    top_5_scorers = sorted(final_players_list, key=lambda x: x.goals_90, reverse=False)[-6:-1]

    str_data = serialize('json', top_5_scorers)
    data = json.loads(str_data)
    test_var = str_data[1000:1030]

    return render(request, 'myapp/top_scorers_chart.html', {'data': data, 'test_var': test_var})


def compare_players(request):
    chosen_player_name = request.GET.get('search-compare') #this is what we get back from js - selected player long name
    player_1_id = request.GET.get('player_1_id')   
    all_players_names_id_dict = get_name_id_dict(player_1_id) 
    for player_name, player_id in all_players_names_id_dict.items():
        if player_name == chosen_player_name:
            player_2_id = player_id
    player_1_obj = Player.objects.get(player_id=player_1_id)
    player_2_obj = Player.objects.get(player_id=player_2_id)
    player_1_obj_js = player_1_obj.get_attrs_values_dict()
    player_2_obj_js = player_2_obj.get_attrs_values_dict()
    test_var = 'player_1_obj'
    test_var2 = 'player_2_obj'
    context = {
        'test_var': test_var,
        'test_var2': test_var2,
        'chosen_player_name': chosen_player_name,
        'player_1_id': player_1_id,
        'player_1_obj': player_1_obj,
        'player_2_obj': player_2_obj,
        'player_1_obj_js': player_1_obj_js,
        'player_2_obj_js': player_2_obj_js,
    }
    return render(request, 'myapp/compare_players.html', context)

def find_similar(request):
    player_1_id = request.POST.get('player_1_id')
    player_1_obj = Player.objects.get(player_id=player_1_id)
    queryset_list = Player.objects.filter(~Q(player_id=player_1_id), cc_90__gte=player_1_obj.cc_90-0.21, cc_90__lte=player_1_obj.cc_90+0.21, total_sb_index__gte=player_1_obj.total_sb_index-40, total_sb_index__lte=player_1_obj.total_sb_index+40, position__icontains=player_1_obj.position_general)
    nothing_found = f'There is only one {player_1_obj.full_name}. No one to compare!'
    return render(request, 'myapp/find_similar.html', {'queryset_list': queryset_list, 'player_1_obj': player_1_obj, 'nothing_found': nothing_found})
