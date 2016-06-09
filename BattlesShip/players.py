import copy
import json


ships = {'Aircraft carrier': 5, 'Battleship': 4, 'Submarine': 3,
         'Destroyer': 3, 'Patrol boat': 2}


class Player:
    
    def __init__(self, name, board, ships, pk):
        self.name = name
        self.board = board
        self.ships = ships
        self.pk = pk

    def __str__(self):
        return "{}".format(self.pk)
    
