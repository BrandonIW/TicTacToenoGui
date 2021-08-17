
from functools import wraps
import logging
from tkinter import messagebox
from random import choice

class TicTacToe:

    players = ("X", "O")                                                    # Class attribute with our players



    def __init__(self):
        self.board = [' ' for _ in range(9)]                                # Create our board with a string of 9 spaces


    def _logger(func):
        logging.basicConfig(filename=f"{func.__name__}", level=logging.INFO)
        def wrapper(self, *args,**kwargs):
            logging.info(f" Player {args[0]} chose space {args[1]}")
            return func(self, *args,**kwargs)
        return wrapper


    def _confirm_valid_input(*vars):    #vars[0] is " " vars[1] is class integer
        def inner(func):                #args[1] is the idex parameter from def edit_square. Which should be a num
            @wraps(func)
            def wrapper(self, *args, **kwargs):

                if len(str(args[1])) == 1 and isinstance(args[1],int) and self.board[args[1]] == vars[0]: # Is my chosen square 1 digit and is my chosen square an int
                                                                                                          # and is my chosen square currently empty
                    TicTacToe.players = TicTacToe.players[::-1]     # Verify that the input is valid. If so, we can swap players
                    return func(self, *args,**kwargs)

                elif isinstance(args[1],str):
                    print("Must be a single integer")

                elif len(str(args[1])) > 1:
                    print(f"Must be a single number between 0-8.")

                else:                                               # If the value of our board at index args[1] does not equal an empty string, then it's currently
                    print("Space already taken")                    # used

            return wrapper
        return inner


    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:             # Print the board. We take indexes 0-2 then
            print('| ' + ' | '.join(row) + ' |')                            # 3-5 then 6-8 etc.


    def main(self):                                                          # Start our game.
                                                        # While there is no winner, print the board
        print(f"Current player is {TicTacToe.players[0]}")
        self.print_board()                                               # and ask to choose a square
        self.edit_square(TicTacToe.players[0],self.choose_square())      # X starts first

        if self.check_winner():
            self.play_again_winner(TicTacToe.players[1])

        elif self.check_tie():
            self.play_again_tie()

        else:
            self.main_ai()

    def main_ai(self):

        print(f"Current player is {TicTacToe.players[0]}")
        self.print_board()                                                          # and ask to choose a square
        self.edit_square(TicTacToe.players[0],choice(self._available_moves()))      # X starts first

        if self.check_winner():
            self.play_again_winner(TicTacToe.players[1])

        elif self.check_tie():
            self.play_again_tie()

        else:
            self.main()

    def choose_square(self):
        try:
            return int(input("Choose a square between 0-8: "))

        except ValueError:
            return f"Must be an integer"


    @_logger
    @_confirm_valid_input(" ",int)
    def edit_square(self, player, idex):
        self.board[idex] = player


    def check_winner(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:       # Get index 0,1,2 and that's a row
            if "".join(row) == "XXX" or "".join(row) == "OOO":
                return True

        for column in [self.board[i*1:(i+7):3] for i in range(3)]:   # Finally got this. Start at index 0, end at index 7 (0+7). Step by 3. That gives you index 0,3,6
            if "".join(column) == "XXX" or "".join(column) == "OOO": # Then next iteration. Start at index 1. End at 8. Step by 3. That gives you index 1,4,7
                return True

        for diagonal in [self.board[i*1::4] for i in range(1)]:
            if "".join(diagonal) == "XXX" or "".join(diagonal) == "OOO":
                return True

        for diagonal in [self.board[2:7:2]]:
            if "".join(diagonal) == "XXX" or "".join(diagonal) == "OOO":
                return True

        return False


#### Here we need to check if all 9 indexes of the playing board are filled up
    def check_tie(self):
        return not any([square for square in self.board if square == " "])


#### Play again function for tie
    def play_again_tie(self):
        if messagebox.askyesno(title="It was a tie",message="Play again?"):
            self.board = [' ' for _ in range(9)]
            self.main()
        else:
            print("You've exited the game")
            quit()

#### Play again function for a winner
    def play_again_winner(self,player):
        if messagebox.askyesno(title=f"Player {player} won",message="Play again?"):
            self.board = [' ' for _ in range(9)]
            self.main()
        else:
            print("You've exited the game")
            quit()

#### Check available moves (for computer player)
    def _available_moves(self):
        return [i for i,spot in enumerate(self.board) if spot == " "] # Create a new list with the index for each possible available move at any given point




if __name__ == '__main__':
    game1 = TicTacToe()
    game1.main()