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

        self.data_import()

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
        self.items['Knife'] = dict(price=12, desc="Pointy staby thing...")
        self.items['Money'] = dict(price=-1, desc="Green goodness, that fuels your purchasing adventures.")

        # This makes sure that every room has an instance of item positions, even if it has no items.
        for room in self.rooms:
            self.item_positions[room] = {}

    # This saves the current rooms, items, and item positions.
    def save_to_file(self):
        joined_dict = {"rooms": self.rooms, "items": self.items, "item_pos": self.item_positions}
        json = dumps(joined_dict, indent=2)
        time = datetime.now()
        with open(f"{time.date()}-{time.hour}.{time.minute}-room.json", 'w') as file:
            file.write(json)
        return

    @staticmethod
    def retrieve_local_rooms():
        return glob("*-room.json")
    @staticmethod
    def retrieve_local_players():
        return glob("*-player.json")

    def replace_data(self, chosen_file):
        with open(chosen_file, 'r') as file:
            data = load(file)
            self.rooms = data['rooms']
            self.items = data['items']
            self.item_positions = data['item_pos']
