import sys


class Ui:
    @staticmethod
    def show_menu():
        print("""WELCOME""")
        print("Retrieve from file (1) or load sample (2)")

        user_input = input().strip()

        if user_input != "1" and user_input != "2":
            sys.exit(255)
        else:
            return int(user_input)

    def menu_selection(self):
        pass

    @staticmethod
    def import_file(files):
        print(f"There was {len(files)} {'files' if len(files) > 1 else 'file'} found.")
        i = 0
        for file in files:
            i += 1
            print(f"    {i}. {file}")
        try:
            num = int(input("Which file would you like to import? (Type 0 to cancel)\n"))
            if num == 0:
                return ""
            else:
                return files[num]
        except ValueError:
            print("Invalid value, returning to menu.")
            return ""
        except IndexError:
            print("Invalid value, returning to menu.")
            return ""
