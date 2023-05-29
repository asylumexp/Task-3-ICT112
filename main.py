from datastore import DataStore
from ui import Ui

data_store = DataStore()
ui = Ui()


def main():
    user_input = ui.show_menu()

    match user_input:
        case 1:
            files = data_store.retrieve_local_rooms()
            chosen_file = ui.import_file(files)
            if chosen_file == "":
                main()
            else:
                data_store.replace_data(chosen_file)
        case 2:
            data_store.data_import()


if __name__ == "__main__":
    main()
