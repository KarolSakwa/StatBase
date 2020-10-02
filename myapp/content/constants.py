# for reusable custom template with tables
SCORERS_ATTRS_NAMES = ["Goals scored", "Games played", "Minutes played", "Goals/90 minutes"]
AGGRESSION_ATTRS_NAMES = ["Games played", "Yellow cards", "Red cards", "Yellow cards per 90 minutes", "Red cards per 90 minutes", "SB aggression index"]
ASSISTANTS_ATTRS_NAMES = ["Assists", "Games played", "Minutes played", "Assists/90 minutes"]
SCORERS_ATTRS = ["goals", "played_games", "minutes", "goals_90"]
AGGRESSION_ATTRS = ["played_games", "yellow_cards", "red_cards", "yc90", "rc90", "sb_aggression_index"]
ASSISTANTS_ATTRS = ["assists", "played_games", "minutes", "assists_90"]
SB_INDEX_ATTRS_NAMES = ["Games played", "Goals", "Assists", "Minutes", "Goals/90 minutes", "Assists/90 minutes", "SB Index"]
SB_INDEX_ATTRS = ["played_games", "goals", "assists", "minutes", "goals_90", "assists_90", "total_sb_index"]
INJURY_PRONE_ATTRS_NAMES = ["Games played", "Minutes", "SB index", "Total days injured", "Games missed"]
INJURY_PRONE_ATTRS = ["played_games", "minutes", "total_sb_index", "total_days_injured", "total_games_injured"]


# League weights for SB index calculation - for now it's assigned by subjectively by me, eventually I'd like it to be calculated in some objective way

leagues_weights = {
    'LaLiga2': 3,
	'NASL Playoffs': 2,
	'US Open Cup': 1,
	'DFL-Supercup': 4,
	'UEFA Super Cup': 4,
	'FIFA Club World Cup': 4,
	'AFC Champions League': 3,
	'DFB-Pokal': 3,
	'NASL Spring Championship': 2,
	'Europa League': 4,
	'NASL Fall Championship': 2,
	'Qatar Stars League': 3,
	'Bundesliga': 5,
	'Intercontinental Cup': 3,
	'Play-Out Serie A': 5,
	'Recopa Sudamericana': 3,
	'UEFA Champions League Qualifying': 4,
	'Supercopa': 5,
	'TOTO KNVB beker': 2,
	'Coppa Italia': 3,
	'UEFA Cup Winners Cup': 4,
	'Copa del Rey': 3,
	'Copa Libertadores': 4,
	'UEFA-Cup': 4,
	'Campeonato Brasileiro Série A': 4,
	'UEFA Champions League': 5,
	'Eredivisie': 4,
	'Serie A': 5,
	'LaLiga': 5,
    'National Team': 6,
	'Premier Liga': 3, 
	'Premier League': 5, 
	'Ukrainian Cup': 2, 
	'FA Cup': 3, 
	'EFL Cup': 3, 
	'Supercoppa Italiana': 5, 
	'Community Shield': 5, 
	'Ukrainian Super Cup': 3, 
	'Johan Cruijff Schaal': 2,
	'UEFA Intertoto Cup': 3, 
	'Ligue 1': 4, 
	'Ligue 2': 3, 
	'Süper Lig': 3, 
	'Major League Soccer': 3, 
	'USL Championship': 3, 
	'Chinese Super League': 3, 
	'Coupe de la Ligue': 2, 
	'Coupe de France': 2, 
	'MLS Cup Playoffs': 2, 
	'USLC Playoffs': 3, 
	'Türkiye Kupasi': 2, 
	'Canadian Championship': 3, 
	'TFF Süper Kupa': 2, 
	'Championship': 4, 
	'Europa League Qualifying': 3, 
	'Premier League 2': 2,
}