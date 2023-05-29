import sys
import os
if sys.platform == "win32":
    import msvcrt
else:
    import termios
    import tty


class Ui:
    def __init__(self):
        self.selection = 0
        self.welcome = """WELCOME"""

    def show_menu(self):
        self.get_menu_selection(["Import rooms from file", "Import sample rooms", "Quit"])
        return self.selection

    def import_file(self, files: list):
        files.append("Return to main menu")
        self.get_menu_selection(files)

        if self.selection == len(files)-1:
            return -1
        else:
            return files[self.selection]

    def check_player_data(self, players):
        players.append("Continue as new player")
        self.get_menu_selection(players)

    def get_menu_selection(self, menu):
        """
            Description:
                Uses self.captureKeys to get the pressed key and make subsequent changes. If pressed key is enter 
                then it returns to the main function so that the menu can change what is shown.
        """

        self.print_options(menu)
        while True:
            key = self.capture_keys(max_k=11)
            if key == "up" or key == "down":
                self.print_options(menu)
            elif key == "enter":
                return

    def print_options(self, menu: list):
        """
            Description:
                Prints all the main menu options,
                changing colours and adding indicators for selected options.
        """

        self.clear_screen()
        print('\x1b[1;130;44m', self.welcome, '\x1b[0m')

        # * Print options on screen
        for option in range(len(menu)):
            # * Show indicator if current selected matches option
            if self.selection == option:
                print('\x1b[6;30;42m' + "<•>", menu[option], '\x1b[0m')
            else:
                print("<○>", menu[option])

    @staticmethod
    def clear_screen():
        """
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

    @staticmethod
    def getch(char_width=1):
        """
            Description:
                Gets pressed key and returns it

            Args:
                char_width (int, optional): character width. Defaults to 1.

            Returns:
                pressed key (unicode character):Returns the pressed key as a unicode character
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
