# Generated by Django 3.0.7 on 2020-07-08 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('season', models.IntegerField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=500, null=True)),
                ('long_name', models.CharField(blank=True, max_length=500, null=True)),
                ('player_id', models.IntegerField()),
                ('profile_img_url', models.URLField(blank=True, max_length=1500, null=True)),
                ('nationality', models.CharField(blank=True, max_length=500, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=500, null=True)),
                ('position', models.CharField(blank=True, max_length=50, null=True)),
                ('position_general', models.CharField(blank=True, max_length=50, null=True)),
                ('club', models.CharField(blank=True, max_length=50, null=True)),
                ('club_img_url', models.URLField(blank=True, max_length=1500, null=True)),
                ('national_team', models.CharField(blank=True, max_length=50, null=True)),
                ('national_team_img_url', models.URLField(blank=True, max_length=1500, null=True)),
                ('played_seasons', models.IntegerField(blank=True, null=True)),
                ('played_games_club', models.IntegerField(blank=True, null=True)),
                ('played_games_national', models.IntegerField(blank=True, null=True)),
                ('played_games', models.IntegerField(blank=True, null=True)),
                ('total_games_injured', models.IntegerField(blank=True, null=True)),
                ('total_days_injured', models.IntegerField(blank=True, null=True)),
                ('goals_club', models.IntegerField(blank=True, null=True)),
                ('goals_national', models.IntegerField(blank=True, null=True)),
                ('goals', models.IntegerField(blank=True, null=True)),
                ('assists_club', models.IntegerField(blank=True, null=True)),
                ('assists_national', models.IntegerField(blank=True, null=True)),
                ('assists', models.IntegerField(blank=True, null=True)),
                ('minutes_club', models.IntegerField(blank=True, null=True)),
                ('minutes_national', models.IntegerField(blank=True, null=True)),
                ('minutes', models.IntegerField(blank=True, null=True)),
                ('cc', models.IntegerField(blank=True, null=True)),
                ('goals_90', models.FloatField(blank=True, null=True)),
                ('assists_90', models.FloatField(blank=True, null=True)),
                ('cc_90', models.FloatField(blank=True, null=True)),
                ('yellow_cards', models.IntegerField(blank=True, null=True)),
                ('red_cards', models.IntegerField(blank=True, null=True)),
                ('total_cards_weighted', models.IntegerField(blank=True, null=True)),
                ('yc90', models.FloatField(blank=True, null=True)),
                ('rc90', models.FloatField(blank=True, null=True)),
                ('sb_aggression_index', models.FloatField(blank=True, null=True)),
                ('seasons_active', models.CharField(blank=True, max_length=500, null=True)),
                ('goals_types_club', models.CharField(blank=True, max_length=500, null=True)),
                ('goals_types_national', models.CharField(blank=True, max_length=500, null=True)),
                ('goals_types', models.CharField(blank=True, max_length=500, null=True)),
                ('leagues_dict', models.CharField(blank=True, max_length=50000, null=True)),
                ('sb_index_by_league', models.CharField(blank=True, max_length=50000, null=True)),
                ('total_sb_index', models.FloatField(blank=True, null=True)),
                ('season_competition_stats', models.CharField(blank=True, max_length=50000, null=True)),
                ('detailed_stats', models.CharField(blank=True, max_length=50000, null=True)),
                ('views_count', models.IntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('num_updates', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Searches',
            },
        ),
    ]
