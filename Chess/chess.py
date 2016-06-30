import copy
import json
import os
import sys


""" king: K, queen: Q, rook: R, bishop: B, knight; N, pawn: P player1: *, player2: +  """


def clear():
    """ Clears the screen """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



def line_up_board(num, sym):
    """ puts in pieces of line 1 or 7 """
    king = "K"
    queen = "Q"
    if sym == "+":
        king ="Q"
        queen = "K"
    return {num+"a":sym+"R", num+"b": sym+"N", num+"c": sym+"B",
            num+"d": sym+queen, num+"e": sym+king, num+"f": sym+"B",
            num+"g": sym+"N", num+"h": sym+"R"}


def chess_board():
    """ makes a dict which holds initial set up of chess board """
    board = {**line_up_board("1", "*"), **line_up_board("8", "+")}
    for num in range(2,8):
        for letter in 'abcdefgh':
            box = "{}{}".format(num, letter)
            if num == 2:
                board[box] = "*P"
            elif num == 7:
                board[box] = "+P"
            else:
                board[box] = '0'
    return board


def draw_board(board):
    """ draws chess board with all pieces """
    box = ""
    print(board["7a"])
    print(" | a| b| c| d| e| f| g| h")
    for num in range(1,9):
        print("{}|".format(num), end='')
        for letter in "abcdefgh":
            box = "{}{}".format(num, letter)
            if board[box] == '0':
                print("  |", end='')
            else:
                print("{}|".format(board[box]), end='')
        print("")


def pawn_moves(board, position, player, opponent):
    """ return valid moves for pawn """
    moves = []
    letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    position = list(position)
    left = ""
    right = ""
    if player == "+":
        ahead = "{}{}".format(int(position[0]) - 1, position[1])
        left = "{}{}".format(
            int(position[0]) - 1,
            letter_list[letter_list.index(position[1]) - 1])
        right = "{}{}".format(
            int(position[0]) - 1,
            letter_list[letter_list.index(position[1]) + 1])
        if board[ahead] == '0':
            moves.append(ahead)
        if position[0] == '7':
            moves.append("5{}".format(position[1]))
    if player == "*":
        ahead = "{}{}".format(int(position[0]) + 1, position[1])
        left = "{}{}".format(
            int(position[0]) + 1,
            letter_list[letter_list.index(position[1]) - 1])
        right = "{}{}".format(
            int(position[0]) + 1,
            letter_list[letter_list.index(position[1]) + 1])
        if board[ahead] == '0':
            moves.append(ahead)
        if position[0] == '2':
            moves.append("4{}".format(position[1]))
    try:            
        if opponent in board[left]:
            moves.append(left)
    except KeyError:
        pass
    try:
        if opponent in board[right]:
            moves.append(right)
    except KeyError:
        pass
    return moves


def rooks_moves(board, position, player, opponent):
    """ returns a liat with all valid moves for rook at given position"""
    moves = []
    letter_list = ['n', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    position = list(position)
    num = int(position[0])
    letter = position[1]
    box = ""
    for place in range(num+1, 9):
        box = "{}{}".format(place, letter)
        if opponent in board[box]:
            moves.append(box)
            break
        elif player in board[box]:
            break
        moves.append(box)
    for place in letter_list[letter_list.index(letter)+1:]:
        box = "{}{}".format(num, place)
        if opponent in board[box]:
            moves.append(box)
            break
        elif player in board[box]:
            break
        moves.append(box)
    for place in letter_list[letter_list.index(letter)-1:0:-1]:
        box = "{}{}".format(num, place)
        if opponent in board[box]:
            moves.append(box)
            break
        elif player in board[box]:
            break
        moves.append(box)
    for place in range(1, num):
        place = num - place
        box = "{}{}".format(place, letter)
        if opponent in board[box]:
            moves.append(box)
            break
        elif player in board[box]:
            break
        moves.append(box)
    return moves


def bishops_moves(board, position, player, opponent):
    """ returns all valid moves for bishop """
    position = list(position)
    num = int(position[0])
    letter = position[1]
    moves = ((bishop_checker(board, num, letter, player, opponent, "++")) +
            (bishop_checker(board, num, letter, player, opponent, "+-")) +
            (bishop_checker(board, num, letter, player, opponent, "-+")) +
            (bishop_checker(board, num, letter, player, opponent, "--")))
    return moves


def queens_moves(board, position, player, opponent):
    """ returns all valid moves for queen """
    psition = list(position[0])
    num = int(position[0])
    letter = position[1]
    moves = (bishop_checker(board, num, letter, player, opponent, "++") +
             bishop_checker(board, num, letter, player, opponent, "+-") +
             bishop_checker(board, num, letter, player, opponent, "-+") +
             bishop_checker(board, num, letter, player, opponent, "--") +
             rooks_moves(board, position, player, opponent))
    return moves


def bishop_checker(board, num, letter, player, opponent, direction):
    """ loops diagnally accross screen from position to X and checks if good"""
    moves = []
    letter_list = ['n', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    box = ""
    for numb in range(1, 7):
        let = numb
        if direction == "+-":
            let = -numb
        elif direction == "-+":
            numb = -numb
        elif direction == "--":
            numb = -numb
            let = numb
        try:
            box = "{}{}".format(
                num+numb,
                letter_list[letter_list.index(letter)+let]
            )
            if opponent in board[box]:
                moves.append(box)
                break
            elif player in board[box]:
                break
            moves.append(box)
        except KeyError:
            break
        except IndexError:
            break
    return moves

    
def kings_moves(position):
    """ return all spaces around a given piece. (used by king) """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    position = list(position)
    num = int(position[0])
    letter = position[1]
    moves = ["{}{}".format(num + 1, letters[letters.index(letter) - 1]),
             "{}{}".format(num + 1, letter),
             "{}{}".format(num + 1, letters[letters.index(letter) + 1]),
             "{}{}".format(num, letters[letters.index(letter) - 1]),
             "{}{}".format(num, letters[letters.index(letter) + 1]),
             "{}{}".format(num - 1, letters[letters.index(letter) - 1]),
             "{}{}".format(num - 1, letter),
             "{}{}".format(num - 1, letters[letters.index(letter) + 1])]
    return moves


def knight_moves(position):
    """ returns all posiible moves for a knight at any point of game"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    position = list(position)
    num = int(position[0])
    letter = position[1]
    moves = ["{}{}".format(num + 1, letters[letters.index(letter) - 2]),
             "{}{}".format(num + 2, letters[letters.index(letter) - 1]),
             "{}{}".format(num - 1, letters[letters.index(letter) - 2]),
             "{}{}".format(num - 2, letters[letters.index(letter) - 1]),
             "{}{}".format(num + 2, letters[letters.index(letter) + 1]),
             "{}{}".format(num - 2, letters[letters.index(letter) + 1]),
             "{}{}".format(num + 1, letters[letters.index(letter) + 2]),
             "{}{}".format(num - 1, letters[letters.index(letter) + 2])]
    return moves


def king_knight_moves(board, position, player, opponent, piece):
    """ returns all moves allowed for king (at present king could check
    himself) and knight
    """
    moves = ""
    if piece == "K":
        moves = kings_moves(position)
    elif piece == "N":
        moves = knight_moves(position)
    good_moves = []
    for move in moves:
        try:
            if piece == "K":
                if (player not in board[move]
                  and check(board, opponent, player, move) == False
                ):
                    good_moves.append(move)
            else:
                if player not in board[move]:
                    good_moves.append(move)
        except TypeError:
            pass
        except KeyError:
            pass
    return good_moves





def turn(board, player):
    """ does each turn """
    start = ""
    end = ""
    moves = []
    opponent = "+"
    if player == "+":
        opponent = "*"
    while True:
        start = input("Which box do you want to move:  ").lower()
        try:
            if player in board[start]:
                moves = all_moves(board, start, player, opponent)
                if len(moves) > 0:
                    break
                else:
                    print("Sorry no available moves!")
        except TypeError:
            print("ERROR")
        except KeyError:
            pass
    while True:
        print("You picked {} at {} box. you could move to {}".format(
            board[start], start, ', '.join(moves)))
        end = input("Where do you want to move: ")
        if end == "cancel":
            turn(board, player)
        elif end in moves:
            if "K" in board[end]:
                print("CHECK MATE!!! /n/n {} won!".format(player))
                sys.exit(0)
            board[end] = board[start]
            board[start] = '0'
            if board[end] == "+P" and "1" in end:
                board[end] = "+Q"
            elif board[end] == "*P" and "8" in end:
                board[end] = "*Q"
            break


def all_moves(board, start, player, opponent):
    """ returns all available moves for given piece """
    moves = ""
    if "P" in board[start]:
        moves = pawn_moves(board, start, player, opponent)
    elif "N" in board[start]:
        moves = king_knight_moves(board, start, player, opponent, "N")
    elif "K" in board[start]:
        moves = king_knight_moves(board, start, player, opponent, "K")
    elif "R" in board[start]:
        moves = rooks_moves(board, start, player, opponent)
    elif "B" in board[start]:
        moves = bishops_moves(board, start, player, opponent)
    elif "Q" in board[start]:
        moves = queens_moves(board, start, player, opponent)
    return moves


def check(board, opponent, player, king):
    """ checks if king is in check """
    checked = False
    for box in board:
        if opponent in board[box] and "K" not in board[box]:
            moves = all_moves(board, box, player, opponent)
            if king in moves:
                checked = True
    return checked


def check_mate(board, opponent, player, king):
    """ checks if king is in check mate """
    if check(board, opponent, player, king):
        print("Check")
        kings_moves = king_knight_moves(board, king, player, opponent, "K")
        if len(kings_moves) < 1:
            print("CHECK MATE!!! /n/n {} won!".format(player))
            sys.exit(0)
        else:
            print("You could move king {}".format(kings_moves))

# board = chess_board()
# draw_board(board)
# print(check_mate(board, "*", "+", "3b"))


def save(board):
    """ saves current progress of game """
    saved_game = open('chess.json', 'w')
    json.dump(board, saved_game, sort_keys=True)
    saved_game.close


def load_game():
    """ loads game from chess.json"""
    saved_game = open('chess.json', 'r')
    board = json.load(saved_game)
    saved_game.close
    return board


def rules():
    """ prints rules of game """
    print(""" Welocome to chess!


    The goal of chess is to get the oppenents king into a checkmate!
    In this game you actually have to kill the king to win

    This is a two player game so get a friend!
    One player will be reperseted by '+' and another by '*' so remember you sign
    You play by passing the computer around after each turn to oter player!

    The board is a grid 1-8 and a-h. The number goes before the letter like 5b.
    Each turn the console will print the board and prompt you for a move.
    So type in the box of the piece you want to move and if its a valid piece
    the console will prompt you for where you want to move it and give you all
    options. Make sure to type in the grid number like 5b and not the symbol
    like +N. If you typed a valid move the piece will move removing thats there.
    You could always type cancel to restart move.

    After each set of turn the computer will prompt for diffrent options.
    Type 'save' to save game, 'quit' to quit game (it will give you the option
    to save), 'help' to get rules and keys (this message) and 'restart' to
    start a new game!\


    KEYS:
    player1 = +      player2 = *
    K = King         Q = Queen       B = Bishop
    R = Rook         P = Pawn        N = Knight

    each piece is displayed player symbol first then piece key like *N or +P

    
    """)


def options(board):
    """ allows players to save game, quit game, get help or restart """
    action = input("do you want any action(help/save/quit/restart):  ").lower()
    if action == 'save':
        save(board)
        print("\n\n Game Saved!\n")
    elif action == 'quit':
        to_save = input("do you want to save:  ")
        if to_save == 'yes':
            save(board)
        print("Exiting....")
        sys.exit(0)
    elif action == 'help':
        rules()
    elif action == 'restart':
        game()
    



def start_game():
    """ starts game allowing user to restart game or continue from old game """
    rules()
    new_game = input("Do you want to start a new game?  ")
    board = ""
    if new_game.lower() != 'yes':
        try:
            board = load_game()
            return board
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
    return chess_board()
        
    
def game():
    """ intire program game of chess"""
    clear()
    board = start_game()
    options(board)
    while True:
        draw_board(board)
        print("", end='\n\n')
        print("+ turn:")
        turn(board, "+")
        draw_board(board)
        print("", end='\n\n')
        print("* turn:")
        turn(board, "*")
        options(board)


game()
