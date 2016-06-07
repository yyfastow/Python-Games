import copy
import json


ships = {'Aircraft carrier': 5, 'Battleship': 4, 'Submarine': 3,
         'Destroyer': 3, 'Patrol boat': 2}


class Player:
    ships = ships
    
    def __init__(self, name, board, pk):
        self.name = name
        self.board = board
        self.pk = pk

    def __str__(self):
        return "{}".format(self.pk)
    
