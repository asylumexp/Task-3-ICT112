import sys
import os
from time import sleep
from random import randint

if sys.platform == "win32":
    import msvcrt
else:
    import termios
    import tty


class Ui:
    def __init__(self):
        self.end = ""
        self.selection = 0
        self.available_actions = []
        self.test_mode = False

    def show_menu(self):
        """show_menu function\n
        Runs, unless in test mode, immediately upon start and checks if the user wants to load a save
        """
        selection = self.get_menu_selection(["Import rooms from file", "Import sample rooms", "Quit"], "WELCOME")
        return selection

    def wait_for_input(self):
        """wait_for_input function\n
        Gets the user to confirm whether they want to continue or not.
        """
        self.flush_input()
        sleep(.5)
        input(f"{Colours.BLUE}Press Enter to Continue.{Colours.END}\n")
        self.clear_screen()

    def import_file(self, files: list):
        """import_file function\n
        Runs if user chooses to load a save file on first menu. Displays all local rooms from DS.
        """
        files.append("Return to main menu")
        selection = self.get_menu_selection(files, "WELCOME")

        if selection == len(files) - 1:
            return -1
        else:
            return files[selection]

    def check_player_data(self, players):
        """check_player_data function\n
        Local player files is passed from DS to here and is displayed to user as menu.
        """
        players.append("Continue as new player")
        selection = self.get_menu_selection(players, "WELCOME")
        if selection == len(players) - 1:
            name = input("What would you like to have your character's name to be?\n")
            return ["New", name]
        else:
            return ["", players[selection]]

    def start_game(self, player_name: str):
        """start_game function\n
        Initial story sequence plus load section to make it not feel rushed. Uses self.print_text for story sequence.
        """
        print(f"{Colours.HEADER}LOADING{Colours.END}\n")
        sleep(3)
        self.clear_screen()

        self.print_text("You: *groan* ugh", Colours.CYAN)
        self.print_text(f"???: Welcome to your new life {player_name}.", Colours.BOLD)
        self.print_text("Your body jolts from the weird voice, eyes adjusting to the dark.", Colours.UNDERLINE, False)
        self.print_text("You: W- Who's there!?", Colours.CYAN)
        self.print_text("You look around, the room's surprisingly empty", Colours.UNDERLINE, False)
        self.print_text("You notice words on the wall...", Colours.UNDERLINE, False)
        self.print_text("Lobby", Colours.YELLOW)

    def display_actions(self, _, items, holding, extra_text: list):
        """display_actions function\n
        Takes available actions from DS and displays them to the user to choose from.
        """
        display_actions = ["Move", "Inventory"]
        if items:
            display_actions.append("Pickup")
        if holding:
            display_actions.append("Drop")
        display_actions.append("Save")

        extra_text.append("Available Actions:")

        selection = self.get_menu_selection(display_actions, extra_text)

        return display_actions[selection]

    def action(self, action, rooms: dict, items: list, holding: list, money: int):
        """action function\n
        Displays relevant information for each action:
            - If choosing Move, then it allows the user to choose a room and return it to main.
            - If choosing Inventory, allows user to choose an item to use, to open the shop, or return to the main menu.
            - If choosing Drop, shows the items to drop, shows user they will get money back and how much they get back.
            - If choosing Pickup, shows all the items to pick, & shows they cant pick it up if they are holding 3 items.
            - If choosing save, then tells the user its saving and returns to main menu."""
        if action == "Move":
            text = ["To your:", ""]
            actions = []
            for direction in rooms:
                print(rooms)
                if rooms[direction]:
                    text.append(f"    {direction} you can see the {rooms[direction]}")
                    actions.append(direction)

            text.append("")
            text.append("Where would you like to move to?")
            selection = self.get_menu_selection(actions, text)

            self.clear_screen()
            print(f"Moving to the {rooms[actions[selection]]}.")
            sleep(1)

            return rooms[actions[selection]]

        elif action == "Inventory":
            text = [f"You currently have ${money}.", "You are currently holding:"]
            item_display = ['Shop']

            for item in holding:
                text.append(f"    {item[0]}: {Colours.UNDERLINE}{item[1]['desc']}")
                item_display.append(f"Use the {item[0]}")

            text.append(f"    What would you like to do?")
            item_display.append(f"Return to menu")

            selection = self.get_menu_selection(item_display, text)

            match item_display[selection]:
                case 'Shop':
                    return ['Shop']
                case 'Return to menu':
                    return [""]
                case _:
                    return ['Action', selection - 1]

        elif action == "Pickup":
            text = ["You can see:", ""]
            item_display = []
            for item in items:
                text.append(f"    {item[0]}: {Colours.UNDERLINE}{item[1]['desc']}")
                item_display.append(item[0])
            text.append("")
            text.append("Which would you like to pickup?")

            selection = self.get_menu_selection(item_display, text)

            if len(holding) == 3:
                print("You cannot pick this up as you have too many items.")
                print("Returning to menu.")
                sleep(2)
                return -1
            else:
                return selection

        elif action == "Drop":
            text = ["You are holding:", ""]
            item_display = []
            for item in holding:
                text.append(f"    {item[0]}: {Colours.UNDERLINE}{item[1]['desc']}")
                item_display.append(item[0])
            text.append("")
            text.append("Which would you like to drop?")

            selection_item = self.get_menu_selection(item_display, text)

            if holding[selection_item][2] >= 2:
                self.clear_screen()
                print("\n\x1b[1;130;44m Since this has already been used, it cannot be dropped. \x1b[0m")
                confirmation_item = -1

            elif holding[selection_item][1]['use'] != 'None' and holding[selection_item][1]['use'] != 'Money':
                confirmation_item = self.get_menu_selection(["Yes", "No"], ["Dropping the {} "
                                                                            "will only return a portion of it's "
                                                                            "${:.2f} worth"
                                                            .format(item_display[selection_item],
                                                                    holding[selection_item][1]['price']),
                                                                            "Are you sure you want to continue?"])
            else:
                self.print_text("\n\x1b[1;130;44m You cannot drop this. \x1b[0m")
                confirmation_item = -1

            if confirmation_item == 0:
                discount = randint(60, 95)
                mo_discount = holding[selection_item][1]['price'] - (
                            holding[selection_item][1]['price'] * discount / 100)
                print(f"\x1b[1;130;44m You got {discount}% of the value back. \x1b[0m")
                print(f"\x1b[1;130;44m You successfully received "
                      "${:.2f}\x1b[0m".format(round(holding[selection_item][1]['price'] - mo_discount, 2)))
                print(f"\x1b[1;130;44m Returning to menu. \x1b[0m")
                sleep(2.5)
                return [selection_item, round(holding[selection_item][1]['price'] - mo_discount, 2)]
            print(f"\x1b[1;130;44m Returning to menu. \x1b[0m")
            sleep(2.5)
            return -1
        elif "Save":
            print(f"{Colours.HEADER}Saving and exiting{Colours.END}")
            return

    def shop(self, items, prices, money, holding):
        """shop function\n
        Allows user to buy items, checks if they have enough $$, and if they are holding too many items.
        """
        text = "What would you like to buy?"
        item_display = ['Return to menu']
        for i in range(len(items)):
            if prices[i] != -1 and prices != 25:  # * Only the wallet costs 25.
                item_display.append("{}: ${:.2f}".format(items[i], prices[i]))

        selection_item = self.get_menu_selection(item_display, text)

        self.clear_screen()
        if selection_item == 0:
            pass
        elif prices[selection_item - 1] > money:
            print("You do not have the required funds to purchase this.")
        elif holding == 3:
            print("You cannot purchase this as you are holding too many items.")
        else:
            print("Successfully purchased. You now have ${:.2f}".format(money - prices[selection_item - 1]))
            print("Returning to menu...")
            sleep(2.5)
            return [True, selection_item, items[selection_item - 1], money - prices[selection_item - 1]]

        print("Returning to menu...")
        sleep(2.5)
        return [False, "", -1]

    def print_text(self, text: str, colour="", end=True):
        """print_text
        Used to print text during story sequences or other important sequences, prints out character by character.
        """
        sleep(.5)

        if colour:
            print(colour)

        for character in text:
            print(character, end="", flush=True)
            sleep(2.5 / len(text))  # Effectively makes any input take 2.5 seconds to print

        print(Colours.END)

        if end:
            self.wait_for_input()

    def item_used(self, show_to_user):
        """item_used function
        Takes information about used item from DS and displays it to user.
        """
        self.clear_screen()
        self.print_text(show_to_user[0])

    def get_menu_selection(self, menu, text):
        """
            Description:
                Uses self.captureKeys to get the pressed key and make subsequent changes. If pressed key is enter 
                then it returns to the main function so that the menu can change what is shown.
        """
        self.flush_input()
        self.print_options(menu, text)
        while True:
            key = self.capture_keys(max_k=len(menu) - 1)
            if key == "up" or key == "down":
                self.print_options(menu, text)
            elif key == "enter":
                selection = self.selection
                self.selection = 0
                return selection

    def print_options(self, menu: list, text: str | list):
        """print_options function
            Description:
                Prints all the main menu options,
                changing colours and adding indicators for selected options.
        """

        self.clear_screen()
        if isinstance(text, str):
            print('\x1b[1;130;44m', text, '\x1b[0m')
        else:
            for string in text:
                if string:
                    print('\x1b[1;130;44m', string, '\x1b[0m')
                else:
                    print("")

        # * Print options on screen
        for option in range(len(menu)):
            # * Show indicator if current selected matches option
            if self.selection == option:
                print('\x1b[6;30;42m' + "<•>", menu[option], '\x1b[0m')
            else:
                print("<○>", menu[option])

    @staticmethod
    def clear_screen():
        """clear_screen function
            Description:
                Clears screen, with considerations for *nix and Windows operating systems different commands.
        """
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def capture_keys(self, max_k):
        while True:
            # * Capture key input
            key = ord(self.getch())

            # * Switch case for pressed keys
            match key:
                case 13:
                    key = "enter"
                    return key
                case 72:
                    if self.selection == 0:
                        pass
                    else:
                        self.selection -= 1
                        key = "up"
                        return key
                case 80:
                    if self.selection == max_k:
                        pass
                    else:
                        self.selection += 1
                        key = "down"
                        return key
                case 27:
                    print("Exiting.")
                    sys.exit()

    def flush_input(self):
        """flush_input function\n
        Flushes input buffer to prevent preparing inputs, does not run if in test mode.
        """
        if not self.test_mode:
            if sys.platform == "win32":
                while msvcrt.kbhit():
                    msvcrt.getch()
            else:
                # Unix/Linux
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    @staticmethod
    def getch(char_width=1):
        """getch function
            Description:
                Gets pressed key and returns it

            Args:
                char_width (int, optional): character width. Defaults to 1.

            Returns:
                pressed key (unicode): Returns the pressed key as a unicode character
        """

        if sys.platform == "win32":
            key = msvcrt.getch()
            return key
        else:
            # ? Credit = "https://www.reddit.com/r/learnprogramming/comments/10wpkp/python_getch_in_unix/"
            '''get a fixed number of typed characters from the terminal. 
        Linux / Mac only'''
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(char_width)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            # * NIX and Windows systems have different characters for the arrow keys, fixing them to match windows
            if ord(ch) == 65:
                ch = chr(72)
            elif ord(ch) == 66:
                ch = chr(80)
            return ch


class Colours:
    """Colours class
    Allows adding colours to strings without the not human readable text.
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

