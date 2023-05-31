from typing import Dict, Union
from json import dumps, load
from datetime import datetime
from glob import glob


class DataStore:
    def __init__(self):
        # This creates the instances
        self.rooms: Dict[str, Dict[str, Union[int, str, list]]] = {}
        self.items: Dict[str, Dict[str, Union[str, int]]] = {}
        self.item_positions: Dict[str, Dict[str, int]] = {}
        self.player: Dict[str, Union[list, str, int, tuple]] = {}
        self.current_loaded_file: list[str] = []

    # This initialises all the sample rooms.
    def data_import(self):
        # This adds the sample rooms to the data store.
        self.rooms['Lobby'] = dict(posX=0, posY=0, desc="The beginning room..", instructions="Instructions", hints="")
        self.rooms['Master Bedroom'] = dict(posX=-1, posY=0, desc="The Master Bedroom", instructions="Instructions",
                                            hints="")
        self.rooms['Kids room'] = dict(posX=-2, posY=0, desc="Eerily quiet for a children's room",
                                       instructions="Instructions", hints="")
        self.rooms['En suite'] = dict(posX=-2, posY=0, desc="The draft of the open window sends chills down your "
                                                            "spine..", instructions="Instructions", hints="")
        self.rooms['Basement'] = dict(posX=-1, posY=-1, desc="It's quite dark, perhaps some light may be useful..",
                                      instructions="Instructions", hints="")
        self.rooms['Hallway'] = dict(posX=0, posY=-1, desc="If you venture down further, who knows what you could find",
                                     instructions="Instructions", hints="")
        self.rooms['Kitchen'] = dict(posX=0, posY=1, desc="KITCHEN", instructions="Instructions",
                                     hints="")

        # This adds the sample items to the data store.
        self.items['Knife'] = dict(price=12, desc="Pointy stab thing...")
        self.items['Money'] = dict(price=-1, desc="Green goodness, that fuels your purchasing adventures.")

        # This makes sure that every room has an instance of item positions, even if it has no items.
        for room in self.rooms:
            self.item_positions[room] = {}

        self.current_loaded_file.append(self.save_room_to_file())

    def create_player(self, name):
        self.player = dict(name=name, pos=(0, 0), items=[], money=0)
        self.save_player_to_file()

    def save_player_to_file(self):
        json = dumps(self.player, indent=2)
        with open(f"{self.current_loaded_file[0]}_player.json", 'w') as file:
            file.write(json)
        return

    # This saves the current rooms, items, and item positions.
    def save_room_to_file(self):
        joined_dict = {"rooms": self.rooms, "items": self.items,
                       "item_pos": self.item_positions}
        json = dumps(joined_dict, indent=2)
        filename = f"{datetime.now().date()}-{datetime.now().hour}.{datetime.now().minute}"
        with open(f"{filename}_room.json", 'w') as file:
            file.write(json)
        return filename

    @staticmethod
    def retrieve_local_rooms():
        return glob("*_room.json")

    def retrieve_local_players(self):
        return glob(f"{self.current_loaded_file[0]}_player.json")

    def replace_room_data(self, chosen_file: str):
        head, sep, tail = chosen_file.partition('_')
        self.current_loaded_file.append(str(head))
        with open(chosen_file, 'r') as file:
            data = load(file)
            self.rooms = data['rooms']
            self.items = data['items']
            self.item_positions = data['item_pos']

    def replace_player_data(self, file):
        with open(file, 'r') as file:
            data = load(file)
            self.player = data
