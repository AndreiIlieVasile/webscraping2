from PUBG.main import insert_players_from_country_args, insert_continents, insert_countries_from_continent, \
    print_continents, print_countries, print_players, delete_continents, delete_countries, delete_players, close_db


delete_continents()
delete_countries()
delete_players()

insert_continents()
insert_countries_from_continent("Europe")
insert_players_from_country_args()

print_continents()
print_countries()
print_players()

close_db()
