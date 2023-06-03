from typing import Dict, Union, List
from json import dumps, load
from datetime import datetime
from glob import glob


class DataStore:
    def __init__(self):
        # This creates the instances
        self.rooms: Dict[str, Dict[str, Union[int, str, list]]] = {}
        self.items: Dict[str, Dict[str, Union[str, int]]] = {}
        self.item_positions: Dict[str, List[List[Dict[str, Union[str, int]], int]]] = {}
        self.player: Dict[str, Union[str, tuple, list, int]] = {}
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
        self.items['Knife'] = dict(price=12, desc="Pointy stab thing...", use="Attack")
        self.items['Flashlight'] = dict(price=34, desc="Source of light to guide you.", use="Light")
        self.items['Wallet'] = dict(price=-1,
                                    desc="The holder of the green goodness that fuels your purchasing adventures.",
                                    use="Money")

        # This makes sure that every room has an instance of item positions, even if it has no items.
        for room in self.rooms:
            self.item_positions[room] = []

        self.item_positions['Lobby'].append(['Flashlight', self.items['Flashlight'], 1])
        self.item_positions['Lobby'].append(['Wallet', self.items['Wallet'], 1])
        self.item_positions['Kitchen'].append(['Knife', self.items['Knife'], 3])

        self.current_loaded_file.append(self.save_room_to_file())

    def create_player(self, name):
        self.player = dict(name=name, pos=(0, 0), items=[], money=0)
        self.save_player_to_file()

    def player_available_actions(self):
        available_rooms = dict(North="", East="", South="", West="")
        pos_x = self.player["pos"][0]
        pos_y = self.player["pos"][1]
        current_room = ""

        for room in self.rooms:
            room_x = self.rooms[room]["posX"]
            room_y = self.rooms[room]["posY"]

            if room_x == pos_x + 1 and pos_y == room_y:
                available_rooms["East"] = room
            elif room_x == pos_x - 1 and pos_y == room_y:
                available_rooms["West"] = room
            elif room_y == pos_y + 1 and pos_x == room_x:
                available_rooms["North"] = room
            elif room_y == pos_y - 1 and pos_x == room_x:
                available_rooms["South"] = room
            elif room_y == pos_y and pos_x == room_x:
                current_room = room

        return available_rooms, self.item_positions[current_room], self.player["items"]

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

        if len(self.current_loaded_file):
            filename = self.current_loaded_file[0]
        else:
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


