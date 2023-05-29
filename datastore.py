from typing import Dict, Union


class DataStore:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, Union[int, str, list]]] = {}
        self.items: Dict[str, Dict[str, Union[str, int]]] = {}
        self.item_positions: Dict[str, Dict[str, int]] = {}

        self.data_import()

    def data_import(self):
        self.rooms['Lobby'] = dict(posX=0, posY=0, desc="The beginning room..", instructions="Instructions", hints="")
        self.rooms['Master Bedroom'] = dict(posX=-1, posY=0, desc="The Master Bedroom", instructions="Instructions",
                                            hints="")
        self.rooms['Kids room'] = dict(posX=-2, posY=0, desc="Eerily quiet for a children's room",
                                       instructions="Instructions", hints="")
        self.rooms['En suite'] = dict(posX=-2, posY=0, desc="The draft of the open window sends chills down your "
                                                            "spine..", instructions="Instructions", hints="")
        self.rooms['Basement'] = dict(posX=-1, posY=-1, desc="It's quite dark, perhaps some light may be useful..",
                                      instructions="Instructions", hints="")
        self.rooms['Hallway'] = dict(posX=0, posY=-1, desc="May you venture down further, who knows what you could find"
                                     , instructions="Instructions", hints="")
        self.rooms['Kitchen'] = dict(posX=0, posY=1, desc="KITCHEN", instructions="Instructions",
                                     hints="")
