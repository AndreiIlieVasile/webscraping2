from PUBG.main import insert_players_from_country_args, insert_continents, insert_countries_from_continent, \
    insert_games, print_continents, print_countries, print_players, print_games,\
    delete_continents, delete_countries, delete_players, close_db


# delete_continents()
# delete_countries()
# delete_players()

insert_games()
insert_continents("counterstrike")
insert_countries_from_continent("counterstrike", "Asia")
insert_players_from_country_args()

print_games()
print_continents()
print_countries()
print_players()

close_db()
