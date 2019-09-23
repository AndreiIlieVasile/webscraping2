from PUBG.main import (insert_players_from_country_args, insert_continents, insert_countries_from_continent,
                       insert_games, print_continents, print_countries, print_players, print_games, close_db)

# from PUBG.main import delete_continents, delete_countries, delete_players, delete_games
# delete_games()
# delete_continents()
# delete_countries()
# delete_players()

insert_games()
insert_continents(game_name="counterstrike")
insert_countries_from_continent(game_name="counterstrike", continent_name="Oceania")
insert_players_from_country_args()

print_games()
print_continents()
print_countries()
print_players()

close_db()
