from game.station import Station

station = Station()

status = station.get_status()
while True:

    station.update_system("oxygen", -90)

    print(station.get_status())

    if station.is_game_over():
        print("You lose!")
        break
