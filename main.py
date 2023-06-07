import sys
import os
from glob import glob
from random import choice
from time import sleep

from datastore import DataStore
from ui import Ui

data_store = DataStore()
ui = Ui()

new_player = False

test_mode = False


def main(restart=False):
    if os.path.exists("TEST"):
        test()

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
        global new_player
        new_player = True
        data_store.create_player(user_input[1].strip())
    else:
        data_store.replace_player_data(user_input[1].strip())

    game()


def game():
    global new_player
    running = True
    if new_player:
        ui.start_game(data_store.player["name"])
    while running:
        rooms, items, holding, money = data_store.player_available_actions()

        user_action = ui.display_actions(rooms, items, holding, data_store.extra_text)

        result = ui.action(user_action, rooms, items, holding, money)
        data_store.extra_text = []

        if data_store.end_check == "END":
            running = False
            end()
        elif result != -1:
            match user_action:
                case "Move":
                    data_store.move(result)
                case "Inventory":
                    if result[0] == "Shop":
                        items, prices, money = data_store.shop()
                        data_store.purchased(ui.shop(items, prices, money, len(holding)))
                    elif result[0] == "Action":
                        ui.item_used(data_store.used_item(holding, result[1]))
                case "Pickup":
                    data_store.pickup(result)
                case "Drop":
                    data_store.drop(result)
                case "Save":
                    data_store.save_room_to_file()
                    data_store.save_player_to_file()
                    sys.exit()


def test():
    """Testing Function

    Called when main sees that a file called TEST exists in the current directory, it initiates testing, seeing if it
    is possible to complete the game from start through to finish.
    """
    try:
        # Import the keyboard module
        import keyboard

        global test_mode

        '''
        Update the test mode variables to indicate to the end() function in main to not restart and the flush_input()
        function inside UI to not flush input.
        '''
        test_mode = True
        ui.test_mode = True

        # Removes all the JSON save files in the folder, so that a half completed game is not started.
        json_files = glob("*.json")
        for file in json_files:
            os.remove(file)

        # Opens the file called TEST and gets all the key presses from it and telling the keyboard module to hit them.
        with open("TEST", 'r') as file:
            for line in file.readlines():
                line = line.strip()  # Remove leading/trailing whitespace and newline characters
                if line:
                    keyboard.press(line)
                    sleep(.05)  # Sleep for a short duration to simulate key press
                    keyboard.release(line)

    except ModuleNotFoundError:
        # Occurs if the keyboard module is not installed from pip.
        print("Testing not available. Please install 'keyboard' via pip.")


def end():
    global new_player
    global test_mode
    if test_mode:
        print("SUCCESS, game tested successfully from start through finish.")
        sys.exit()
    else:
        ui.print_text("???: It appears you were successful this time", "", False)
        ui.print_text("You: Does that mean I'm able to leave??", "", False)
        ui.print_text(f"???: Maybe next time {data_store.player['name']}")
        data_store.data_import()
        first_names = [
            "John", "Emma", "Michael", "Sophia", "Robert", "Olivia", "David", "Ava",
            "William", "Mia", "James", "Isabella", "Joseph", "Charlotte", "Daniel", "Amelia"]
        name = choice(first_names)
        data_store.create_player(name)
        new_player = True
        game()


if __name__ == "__main__":
    main()
