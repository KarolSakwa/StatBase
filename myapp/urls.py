from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.conf import settings 
from myapp.models import Player


urlpatterns = [
path('', views.home, name='home'),
path('admin/', admin.site.urls),
path('new_search', views.new_search, name='new_search'),
path('player/<int:player_tm_id>', views.player_profile),
path('db_update', views.db_update, name='db_update'),
path('db_updating_page', views.db_updating_page, name='db_updating_page'),
path('js_test', views.js_test, name='js_test'),
path('all_90_scorers', views.all_90_scorers, name='all_90_scorers'),
path('gk_90_scorers', views.gk_90_scorers, name='gk_90_scorers'),
path('df_90_scorers', views.df_90_scorers, name='df_90_scorers'),
path('mf_90_scorers', views.mf_90_scorers, name='mf_90_scorers'),
path('cf_90_scorers', views.cf_90_scorers, name='cf_90_scorers'),
path('most_aggressive', views.most_aggressive, name='most_aggressive'),
path('most_assists', views.most_assists, name='most_assists'),
path('top_scorers_chart', views.top_scorers_chart, name='top_scorers_chart'),
path('compare_players', views.compare_players, name='compare_players'),
path('find_similar', views.find_similar, name='find_similar'),
path('top_players', views.top_players, name='top_players'),
path('injury_prone', views.injury_prone, name='injury_prone'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)