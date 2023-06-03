import sys

from datastore import DataStore
from ui import Ui

data_store = DataStore()
ui = Ui()


def main(restart=False):
    if restart:
        ui.selection = 0

    user_input = ui.show_menu()

    match user_input:
        case 0:
            files = data_store.retrieve_local_rooms()
            chosen_file = ui.import_file(files)
            if chosen_file == -1:
                main(True)
            else:
                data_store.replace_room_data(chosen_file)
        case 1:
            data_store.data_import()
        case 2:
            sys.exit(-1)

    user_input = ui.check_player_data(data_store.retrieve_local_players())

    if user_input[0] == 'New':
        data_store.create_player(user_input[1].strip())
    else:
        data_store.replace_player_data(user_input[1].strip())

    game()


def game():
    running = True
    while running:
        # ui.start_game(data_store.player["name"])
        rooms, items, holding = data_store.player_available_actions()

        user_action = ui.display_actions(rooms, items, holding)

        result = ui.action(user_action, rooms, items, holding)

        match user_action:
            case "Move":
                print(result)
            case "Pickup":
                print(result)
            case "Drop":
                print(result)
            case "Save":
                data_store.save_room_to_file()
                data_store.save_player_to_file()
                sys.exit(0)
        running = False


if __name__ == "__main__":
    main()
