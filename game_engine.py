
#Exceptions
class InvalidField(Exception):
    pass

class ChosenField(Exception):
    pass


class InvalidSize(ValueError):
    pass


class Board:                  # the game board
    def __init__(self,*args,**kwargs):
        size = kwargs.pop('size')
        if size <= 0:
            raise InvalidSize
        self.size = size
        self.moves = 0        # No moves made yet
        self.fields =  dict() # dictionary associating field with numbers
        self.rows = []        # a list of lists that represent rows
        self.initialize_board()

    def initialize_board(self):
        f = 1 # field number
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(f)
                self.fields[f] = (i,j)
                f += 1
            self.rows.append(row)



    def display_board(self):
        for k in range(self.size):
            print('+---------'*self.size,end='')
            print('+')
            for line in range(5):                   # leave space of five lines
                for j in range(self.size):
                    if line == 2:                   # print the field in the second line
                        print('|    {0:2}   '.format(self.rows[k][j]),end='')
                    else:
                        print('|         ',end='')
                print('|')
        print('+---------'*self.size,end='')
        print('+')

    def change_field(self,row,column,sign):
        self.rows[row][column] =  sign

    def enter_move(self, field ,o_turn=True): #True for O and Flase for X
        if (type(field) != int) or (field not in self.fields.keys()) :
            raise InvalidField
        r , c = self.fields[field]
        if self.rows[r][c] == 'X' or self.rows[r][c] == 'O':
            raise ChosenField
        if o_turn:
            self.change_field(r,c,'O')
        else:
            self.change_field(r,c,'X')








def victory_for(board, player):
    sign = 'O' if player == True else 'X'
    # check for row
    for row in board.rows:
        if all(f == sign for f in row):
            return True

    #check for column
    for i in range(board.size):
        for row in board.rows:
            #assume all fields are equal to the sign
            if row[i] != sign:  #otherwise, stop
                break           #no need to continue
        else:
            return True

    #chech for main diagonal
    i = 0
    for row in board.rows:
        if row[i] != sign:
            break
        i += 1
    else:
        return True

    #chech for off diagonal
    i = board.size - 1
    for row in board.rows:
        if row[i] != sign:
            break
        i -= 1
    else:
        return True

    return False # Nobody won yet or a stalemate



def check_move(board,field_number,player):
    valid_move = True
    try:
        board.enter_move(field_number,player)
        return valid_move
    except InvalidField:
        raise InvalidField('Invalid field')
    except ChosenField:
        raise ChosenField('Field already chosen')


def play_again():
    choice = input("Play Again?(y/n)")
    if choice == 'n' or choice == 'N':
        return False
    else:
        return True


def handle_turn(board,player=True): # True for O and False for X
    # this function checks the validity of the move and doesn't return anything concerning this
    valid_move = False # assumption
    while valid_move != True:
        field_number = int(input('Enter field number: '))
        try:
            valid_move = check_move(board, field_number,player)
            board.moves += 1
        except (InvalidField,ChosenField) as e:
            print(e.args[0]) # print the message
            continue




def main():
    while True:
        in_game = True
        n = int(input('Enter board size: '))
        board = Board(size=n)
        nobody_won = False
        player = True # first turn for O
        while in_game:
            board.display_board()
            handle_turn(board,player)
            if victory_for(board,player):
                sign = 'O' if player == True else 'X'
                print('{} won'.format(sign))
                in_game = False
                continue
            if board.moves == size**2:
                in_game = False
                nobody_won = True
            player = not player # switch player by negation
        if nobody_won:
            print('Nobody won')
        choice = play_again()
        if choice == False:
            print('Goodbye')
            break



if __name__ == '__main__':
    main()
