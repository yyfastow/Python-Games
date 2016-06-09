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


def rules():
    print("""Game Objective

The object of Battleship is to try and sink all of the other player's before
they sink all of your ships. All of the other player's ships are somewhere on
his/her board.  You try and hit them by calling out the coordinates of one of
the squares on the board.  The other player also tries to hit your ships by
calling out coordinates.  Neither you nor the other player can see the other's
board so you must try to guess where they are.  Each board in the physical game
has two grids:  the lower (horizontal) section for the player's ships and the
upper part (vertical during play) for recording the player's guesses.

Starting a New Game

Each player places the 5 ships somewhere on their board.  The ships can only
be placed vertically or horizontally. Diagonal placement is not allowed.
No part of a ship may hang off the edge of the board.  Ships may not overlap
each other.  No ships may be placed on another ship.

Once the guessing begins, the players may not move the ships.

The 5 ships are:  AircraftCarrier (occupies 5 spaces), Battleship (4),
Cruiser (3), Submarine (3), and Destroyer (2).  

Playing the Game

Player's take turns guessing by calling out the coordinates. The opponent
responds with "hit" or "miss" as appropriate.  Both players should mark their
board with pegs:  X for hit, + for miss. For example, if you call out F6
and your opponent does not have any ship located at F6, your opponent would
respond with "miss".  You record the miss F6 by placing a + peg on the
lower part of your board at F6.  Your opponent records the miss by placing.

When all of the squares that one your ships occupies have been hit, the ship
will be sunk.   You should announce "hit and sunk".  In the physical game,
a X is placed on the top edge of the vertical board to indicate a sunk ship. 
As soon as all of one player's ships have been sunk, the game ends.

Display

ships display as O, + are missed shots and X re hits
""")


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
    ships_positions = player.ships
    # loop over ships
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
                # checks if proper size
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
                # loops over each word in user input
                if len(position) < 2:
                    # makes sure each box is more then 2
                    print("make sure to type in numbers from grid like A2")
                    break
                num = position[1]
                try:
                    # checks if leeter and number from 1-10 or A-J
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
                    # checks if put in same box twice
                    print("Don't repeat the same spot twice")
                    break
                elif board[database_box] == 'O':
                    # checks if ship allready there
                    print("That spot is allready taken")
                    break
                elif position[0] != letter and int(num) != int(number):
                    # makes sure ship in same line
                    print("Make sure all postions are in same line")
                    break
                elif len(last_position) > 0:
                    # makes sure each box of ship are one after other
                    try:
                        nexts = columns[columns.index(last_position[-1][0]) + 1]
                    except IndexError:
                        nexts = 'J'
                    last_num = int(last_position[-1][1:])
                    if int(num) < last_num:
                        # if num is less (when 10 is one element checks if 9 exists
                        if '9' not in positions:
                            print("Make sure to have a box each after the other")
                    elif int(num) > last_num + 1 or position[0] > nexts:
                        print("Make sure to have a box each after the other")
                        print(num)
                        print(last_num)
                        break
                if ten(position):
                    # appends box to last_position
                    last_position.append(position[0:3])
                else:
                    last_position.append(position[0:2])
            else:
                # if all tests work add ship to board
                ship_list = []
                for position in positions:
                    number = int(position[1]) - 1
                    if ten(position):
                        number = 9
                    box = "{}{}".format(position[0], number)
                    board[box] = 'O'
                    ship_list.append(box)
                ships_positions[ship] = ship_list
                unfit = False
    #in end save
    save_board(player)
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
    saved_ships = open('ships{}.json'.format(player), 'w')
    json.dump(player.ships, saved_ships, sort_keys=True)
    saved_ships.close


def save_name(player):
    """ saves name of player injson file with players pk"""
    name = open('name{}.json'.format(player), 'w')
    json.dump(player.name, name)
    name.close


def get_board(player):
    """gets saved board of given player frojson file """
    saved_board = open('player{}.json'.format(player), 'r')
    board = json.load(saved_board)
    saved_board.close
    return board


def get_ships(player):
    saved_ships = open('ships{}.json'.format(player), 'r')
    ships = json.load(saved_ships)
    saved_ships.close
    return ships


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
                other_player.board[box] = 'X'
                for ship in other_player.ships:
                    if box in other_player.ships[ship]:
                        other_player.ships[ship].remove(box)
                        if len(other_player.ships[ship]) < 1:
                            print("You sunk my {}".format(ship))
                        else:
                            print("You hit a ship")
                break
            else:
                print("You missed")
                other_player.board[box] = '+'
                break
        except KeyError:
            print("Make sure to write proper boxs")
    if won(other_player):
        print("{} Won You sunk all {} ships!".format(player.name, other_player.name))
        sys.exit(0)
    input("Done:  ")
    clear()
    for ship in other_player.ships:
        if action in other_player.ships[ship]:
            if len(other_player.ships[ship]) < 1:
                print("{} sunk our {}".format(player.name, ship))
                break
            elif action in other_player.ships[ship]:
                print("{} hit your ship at {}.\n\n".format(player.name, action))
                break
    else:
        print("{} missed.\n\n".format(player.name))



def won(player):
    won = True
    for ship in player.ships:
        if len(player.ships[ship]) >= 1:
            won = False
    return won


def options(player1, player2):
    action = input("Do you want any action(help/save/quit):  ").lower()
    if action == 'save':
        save_board(player1)
        save_board(player2)
        print("\n\n Game Saved!\n")
    elif action == 'quit':
        save = input("Do you want to save(type no if you don't):  ").lower()
        if save != 'no':
            save_board(player1)
            save_board(player2)
            print("\n\n Game Saved!\n")
        print("Exiting....")
        sys.exit(0)
    elif action == 'help':
        rules()
        
    
    

def new_game():
    """Makes new game by erasing old data and letting players put in ships. """
    player1 = Player(input("Whats your name: "),
                     copy.deepcopy(battleship_board()),
                     copy.deepcopy(ships),
                     1)
    delete = input("Do you want to continue data of last game will be lost: ").lower()
    if delete != 'yes':
        sys.exit(0)
    save_board(player1)
    save_name(player1)
    put_in_ships(player1.board, player1)
    clear()
    player2 = Player(input("Whats your name: "),
                     copy.deepcopy(battleship_board()),
                     copy.deepcopy(ships),
                     2)
    save_board(player2)
    save_name(player2)
    put_in_ships(player2.board, player2)
    while True:
        options(player, other_player)
        turn(player1, player2)
        turn(player2, player1)


def start_game():
    """Begins the game by giving player option to start new game or continue"""
    clear()
    restart = input("New game:  ")
    if restart.lower() == 'yes':
        new_game()
    else:
        player1 = Player(get_name(1), get_board(1), get_ships(1), 1)
        player2 = Player(get_name(2), get_board(2), get_ships(2), 2)
        while True:
            options(player, other_player)
            turn(player1, player2)
            turn(player2, player1)


start_game()

    


