import copy
import json
import os
import sys

from players import Player, ships


def clear():
    """ Clears the screen """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def battleship_board():
    """ Makes empty battleship board """
    board = {}
    for num in range(0,10):
        for letter in 'ABCDEFGHIJ':
            box = '{}{}'.format(letter, num)
            board[box] = 0
    return board


def draw_board(board, varable=1):
    """ prints board """
    print("   A B C D E F G H I J")
    box = ""
    for num in range(1,11):
        if num == 10:
            print("10|", end='')
        else:
            print(" {}|".format(num), end='')
        for letter in 'ABCDEFGHIJ':
            box = "{}{}".format(letter, num - 1)
            if board[box] == 0 or board[box] == varable:
                print(" |", end='')
            else:
                print("{}|".format(board[box]), end='')
        print("")
    print("  " + "*" * 21)


def put_in_ships(board, player):
    """Allows player to put in ships in board, checks if valid and then saves"""
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    ships_positions = copy.deepcopy(player.ships)
    for ship, size in ships.items():
        print("{}'s board:".format(player.name))
        draw_board(board)
        print("{}: {} spaces".format(ship, size))
        print("Which box do you want to fill up (FORMAT ex: E2 E3 E4): ")
        unfit = True
        while unfit:
            positions = input("You have {} spaces to fill:  ".format(size))
            positions = sorted(positions.upper().split())
            print(positions)
            if len(positions) != size:
                print("Make sure to add {} positions".format(size))
                continue
            try:
                letter = positions[0][0]
                number = positions[0][1]
                if ten(positions[0]):
                    number = "10"
            except IndexError:
                pass
            last_position = []
            for index, position in enumerate(positions):
                if len(position) < 2:
                    print("make sure to type in numbers from grid like A2")
                    break
                num = position[1]
                try:
                    if position[0] not in columns or int(num) not in range(1,11):
                        print("make sure to type in numbers from grid like A2")
                        break
                except ValueError:
                    print("make sure to type in numbers from grid like A2")
                    break
                box = position[0:2]
                database_box = "{}{}".format(position[0], int(num) - 1)
                if ten(position):
                    num = 10
                    box = position[0:3]
                    database_box = "{}9".format(position[0])
                if box in last_position:
                    print("Don't repeat the same spot twice")
                    break
                elif board[database_box] == 'O':
                    print("That spot is allready taken")
                    break
                elif position[0] != letter and int(num) != int(number):
                    print("Make sure all postions are in same line")
                    break
                elif len(last_position) > 0:
                    try:
                        nexts = columns[columns.index(last_position[-1][0]) + 1]
                    except IndexError:
                        nexts = 'J'
                    last_num = int(last_position[-1][1:])
                    if int(num) < last_num:
                        if '9' not in positions:
                            print("Make sure to have a box each after the other")
                    elif int(num) > last_num + 1 and position[0] != nexts:
                        print("Make sure to have a box each after the other")
                        print(num)
                        print(last_num)
                        break
                if ten(position):
                    last_position.append(position[0:3])
                else:
                    last_position.append(position[0:2])
            else:
                ship_list = []
                for position in positions:
                    number = int(position[1]) - 1
                    if ten(position):
                        number = 9
                    box = "{}{}".format(position[0], number)
                    board[box] = 'O'
                    ship_list.append(box)
                ships_positions[ship] = ship_list
                print(ships_positions)
                unfit = False
    save_board(board, player)
    draw_board(board)
    input("Done:")
    clear()
    return ships_positions


def ten(position):
    """checks if number in box or action is 10 and returns true or false """
    try:
        if position[1:3] == '10':
            return True
        else:
            return False
    except IndexError:
        return False


def save_board(player):
    """ saves board of player with players pk """
    saved_game = open('player{}.json'.format(player), 'w')
    json.dump(player.board, saved_game, sort_keys=True)
    saved_game.close


def save_name(player):
    """ saves name of player injson file with players pk"""
    name = open('name{}.json'.format(player), 'w')
    json.dump(player.name, name)
    saved_game.close


def get_board(player):
    """gets saved board of given player frojson file """
    saved_board = open('player{}.json'.format(player), 'r')
    board = json.load(saved_board)
    saved_board.close
    return board


def get_name(player):
    """gets name saved in jsonfile """
    saved_name = open('name{}.json'.format(player), 'r')
    name = json.load(saved_name)
    saved_name.close
    return name


def turn(player, other_player):
    """A turn which involves showing board and making attack """
    start = 'no'
    while start != 'yes':
        start = input("Ready {}'s turn:  ".format(player.name)).lower()
    print("opponents's board:")
    draw_board(other_player.board, 'O')
    print("\n\n")
    print("{}'s board:".format(player.name))
    draw_board(player.board)
    box = ""
    action = ""
    while True:
        action = input("Which box do you want to attack:  ").upper()
        try:
            box = "{}{}".format(action[0], int(action[1:]) - 1)
        except ValueError:
            print("Make sure to write proper boxs")
        try:
            if other_player.board[box] == 'O':
                print("You hit a ship")
                other_player.board[box] = 'X'
                break
            else:
                print("You missed")
                other_player.board[box] = '+'
                break
        except KeyError:
            print("Make sure to write proper boxs")
    input("Done:  ")
    clear()
    if other_player.board[box] == 'X':
        print("{} hit your ship at {}.\n\n".format(player.name, action))
    else:
        print("{} missed.\n\n".format(player))
    
    

def new_game():
    """Makes new game by erasing old data and letting players put in ships. """
    player1 = Player(input("Whats your name: "), copy.deepcopy(battleship_board()), 1)
    delete = input("Do you want to continue data of last game will be lost: ").lower()
    if delete != 'yes':
        system.exit(0)
    save_board(player1)
    save_name(player1)
    put_in_ships(player1.board, player1)
    clear()
    player2 = Player(input("Whats your name: "), copy.deepcopy(battleship_board()), 2)
    save_board(player2)
    save_name(player2)
    put_in_ships(player2.board, player2)


def start_game():
    """Begins the game by giving player option to start new game or continue"""
    clear()
    new_game = input("New game:  ")
    if new_game.lower() == 'yes':
        new_game()
    else:
        player1 = Player(get_name(1), get_board(1), 1)
        player2 = Player(get_name(2), get_board(2), 2)


start_game()
while True:
    turn(player1, player2)
    turn(player2, player1)
    


