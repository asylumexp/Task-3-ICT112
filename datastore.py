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
        self.current_room: str = ""
        self.extra_text: list = []
        self.types_used = []
        self.objectives_ran = []

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
        self.rooms['Basement'] = dict(posX=-1, posY=1, desc="There appears to be a dark figure in here",
                                      instructions="It's quite dark, perhaps some light may be useful..",
                                      hints="Something to defend yourself might be useful here.")
        self.rooms['Hallway'] = dict(posX=0, posY=-1, desc="If you venture down further, who knows what you could find",
                                     instructions="Some light may be useful here...", hints="")
        self.rooms['Kitchen'] = dict(posX=0, posY=1, desc="Easy to find plenty of kitchenware here.",
                                     instructions="Instructions",
                                     hints="")
        self.rooms['Entrance'] = dict(posX=0, posY=-2,
                                      desc="There's a giant door with a keyhole in it, perhaps a key is needed?",
                                      instructions="Instructions",
                                      hints="")

        # This adds the sample items to the data store.
        self.items['Knife'] = dict(price=12, desc="Pointy stab thing...", use="Attack")
        self.items['Flashlight'] = dict(price=34, desc="Source of light to guide you.", use="Light")
        self.items['Key'] = dict(price=34, desc="A mysterious key, found in the basement. "
                                                "I would keep a good hold on it.", use="Key")
        self.items['Wallet'] = dict(price=-1,
                                    desc="The holder of the green goodness that fuels your purchasing adventures.",
                                    use="None")

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
                self.current_room = room

        print(self.current_room)
        if self.current_room == "Basement":
            self.basement()
        elif self.current_room == "Entrance":
            self.entrance()
        elif self.current_room == "Hallway":
            self.hallway()
        elif self.current_room == "Outside":
            self.end()

        self.extra_text.insert(0, '')
        self.extra_text.insert(0, self.rooms[self.current_room]['desc'])
        self.extra_text.insert(0, self.current_room)

        return available_rooms, self.item_positions[self.current_room], self.player["items"], self.player['money']

    def move(self, room):
        room_x = self.rooms[room]["posX"]
        room_y = self.rooms[room]["posY"]
        self.player['pos'] = (room_x, room_y)
        for item in range(len(self.player['items'])):
            print(self.player['items'][item][2])
            if self.player['items'][item][2] >= 2:
                self.extra_text.append(f"After using the {self.player['items'][item][0]}, it has now broken.")
                self.types_used.remove(self.player['items'][item][1]["use"])  # Despite what PyCharm says, this is right
                del self.player['items'][item]

    def basement(self):
        if "Basement Figure" not in self.objectives_ran:
            for i in range(len(self.player['items'])):
                if self.player['items'][i][1]['use'] == "Attack":
                    if self.player['items'][i][2] > 0:
                        self.extra_text.append(
                            "Seeing you armed, the dark figure ran away. It dropped some money as it ran...")
                        self.player['money'] += 50
                        self.extra_text.append(f"You now have ${self.player['money']}!")
                        self.objectives_ran.append("Basement Figure")
                        break
            else:
                self.objectives_ran.append("Basement Figure")
                self.extra_text.append("Upon seeing you unarmed, the dark figure stole all of your money and ran off.")
                self.player['money'] = 0
                self.extra_text.append("You now have $0")
        if "Basement Key" not in self.objectives_ran:
            for i in range(len(self.player['items'])):
                if self.player['items'][i][1]['use'] == "Light":
                    if self.player['items'][i][2] > 0:
                        self.extra_text.append(
                            "With the light, you can see a key in the room, perhaps it will be useful..")
                        self.item_positions['Basement'].append(['Key', self.items['Key'], 1])
                        self.objectives_ran.append("Basement Key")

    def hallway(self):
        for i in range(len(self.player['items'])):
            if self.player['items'][i][1]['use'] == "Light":
                if self.player['items'][i][2] > 0:
                    self.extra_text.append(
                        "With the light, you can see a dark figure in the basement,"
                        " perhaps it would be wise to arm yourself beforehand..")

    def entrance(self):
        for i in range(len(self.player['items'])):
            if self.player['items'][i][1]['use'] == "Key":
                if self.player['items'][i][2] > 0:
                    self.extra_text.append(
                        "With the key at your disposal, you unlock the door in front of you, "
                        "revealing what appears to be the outside...")
                    self.rooms['Outside?'] = dict(posX=-3, posY=0,
                                                  desc="???",
                                                  instructions="??",
                                                  hints="?")

    def end(self):
        return "END"

    def shop(self):
        items = []
        prices = []
        for item in self.items:
            items.append(item)
            prices.append(self.items[item]['price'])

        return items, prices, self.player['money']

    def purchased(self, results):
        if results[0]:
            print(self.player['items'][results[1]])
            self.player['items'].append([results[2], self.items[results[2]]])
            self.player['money'] = results[3]
            print(self.player['items'], self.player['money'])

    def drop(self, item: list):
        del self.player['items'][item[0]]
        self.player['money'] += item[1]

    def pickup(self, item: int):
        item_picked = self.item_positions[self.current_room][item]
        # noinspection PyTypeChecker
        item_picked[2] = 0
        self.player['items'].append(item_picked)
        del self.item_positions[self.current_room][item]

    def used_item(self, items, selected):
        self.types_used.append(self.player['items'][selected][1]["use"])  # Despite what PyCharm says, ["use"] is right.

        match self.items[items[selected][0]]['use']:
            case 'Light':
                self.player['items'][selected][2] += 1
                return [f"You switch on the {items[selected][0]}, lighting up the room.", items[selected][0]]
            case 'Attack':
                self.player['items'][selected][2] += 1
                return [f"You arm yourself with the {items[selected][0]}."]
            case _:
                return [f"You cannot use this."]

    def save_player_to_file(self):
        self.player['objectives'] = self.objectives_ran
        json = dumps(self.player, indent=2)
        with open(f"{self.current_loaded_file[0]}_player.json", 'w') as file:
            file.write(json)

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
            self.objectives_ran = data['objectives']
            self.player = data
